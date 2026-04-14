"""Run the automatable subset of compliance framework checks using Playwright.

Takes the browser page/context and banner detection results, then evaluates
each check marked automated=True and returns Finding objects for the report.
"""

import asyncio

from playwright.async_api import Page, BrowserContext

from ..models import Finding, Status, Severity, BannerDetection, CookieAudit
from ..cookie_inspector import capture_cookies, is_tracking_cookie
from ..banner_detector import _find_banner_element, _extract_buttons
from .compliance_frameworks import ComplianceCheck, ALL_FRAMEWORKS


async def _check_keyboard_accessible(page: Page, banner_locator) -> Finding:
    """WCAG-001: Test keyboard navigation through banner buttons."""
    try:
        buttons = await _extract_buttons(banner_locator)
        if not buttons:
            return Finding(
                criterion="Keyboard accessible (WCAG 2.1.1)",
                status=Status.WARNING,
                detail="No buttons detected in banner — cannot verify keyboard access. Banner may be inside an iframe.",
                severity=Severity.CRITICAL,
            )

        # Tab through the page and check if banner elements receive focus
        await page.keyboard.press("Tab")
        await asyncio.sleep(0.3)

        focused_in_banner = 0
        for _ in range(len(buttons) + 5):
            focused = await page.evaluate("document.activeElement?.tagName + ' ' + (document.activeElement?.textContent || '').trim().substring(0, 50)")
            # Check if the focused element text matches any banner button
            for btn in buttons:
                if btn.lower() in focused.lower():
                    focused_in_banner += 1
                    break
            await page.keyboard.press("Tab")
            await asyncio.sleep(0.2)

        if focused_in_banner >= len(buttons):
            return Finding(
                criterion="Keyboard accessible (WCAG 2.1.1)",
                status=Status.PASS,
                detail=f"All {len(buttons)} banner buttons are reachable via Tab key.",
            )
        elif focused_in_banner > 0:
            return Finding(
                criterion="Keyboard accessible (WCAG 2.1.1)",
                status=Status.WARNING,
                detail=f"Only {focused_in_banner}/{len(buttons)} banner buttons reachable via Tab.",
                severity=Severity.MAJOR,
            )
        else:
            return Finding(
                criterion="Keyboard accessible (WCAG 2.1.1)",
                status=Status.FAIL,
                detail="No banner buttons received focus via Tab key. Banner may not be keyboard accessible.",
                severity=Severity.CRITICAL,
            )
    except Exception as e:
        return Finding(
            criterion="Keyboard accessible (WCAG 2.1.1)",
            status=Status.WARNING,
            detail=f"Could not verify keyboard access: {e}",
            severity=Severity.MAJOR,
        )


async def _check_focus_on_load(page: Page) -> Finding:
    """WCAG-002: Check if focus moves to banner on page load."""
    try:
        focused = await page.evaluate("""() => {
            const el = document.activeElement;
            if (!el || el === document.body) return null;
            return {
                tag: el.tagName,
                role: el.getAttribute('role'),
                ariaLabel: el.getAttribute('aria-label'),
                text: el.textContent?.trim().substring(0, 100),
                inBanner: !!(el.closest('[class*="cookie" i], [class*="consent" i], [id*="cookie" i], [id*="consent" i], [role="dialog"]'))
            };
        }""")

        if focused and focused.get("inBanner"):
            return Finding(
                criterion="Focus on banner at load (WCAG 2.4.3)",
                status=Status.PASS,
                detail=f"Focus is on the banner on page load (element: {focused['tag']}).",
            )
        else:
            return Finding(
                criterion="Focus on banner at load (WCAG 2.4.3)",
                status=Status.WARNING,
                detail="Focus is not on the banner when the page loads. Keyboard/screen-reader users may not notice it immediately.",
                severity=Severity.MAJOR,
            )
    except Exception:
        return Finding(
            criterion="Focus on banner at load (WCAG 2.4.3)",
            status=Status.WARNING,
            detail="Could not determine initial focus state.",
            severity=Severity.MINOR,
        )


async def _check_contrast(page: Page, banner_locator) -> Finding:
    """WCAG-005: Check text contrast ratio in the banner."""
    try:
        contrast_data = await banner_locator.evaluate("""el => {
            const style = window.getComputedStyle(el);
            const bg = style.backgroundColor;
            const fg = style.color;
            const fontSize = parseFloat(style.fontSize);

            // Check buttons too
            const buttons = el.querySelectorAll('button, a, [role="button"]');
            const buttonStyles = [];
            buttons.forEach(btn => {
                const bs = window.getComputedStyle(btn);
                buttonStyles.push({
                    text: btn.textContent?.trim().substring(0, 30),
                    color: bs.color,
                    background: bs.backgroundColor,
                    fontSize: parseFloat(bs.fontSize)
                });
            });

            return { bg, fg, fontSize, buttonCount: buttons.length, buttonStyles };
        }""")

        btn_count = contrast_data.get("buttonCount", 0)
        if btn_count == 0:
            return Finding(
                criterion="Text contrast ratio (WCAG 1.4.3)",
                status=Status.WARNING,
                detail="No buttons found in banner for contrast analysis. Manual verification needed.",
                severity=Severity.MAJOR,
            )

        return Finding(
            criterion="Text contrast ratio (WCAG 1.4.3)",
            status=Status.WARNING,
            detail=f"Banner has {btn_count} interactive element(s). Computed styles captured — verify contrast ratios meet 4.5:1 (normal text) or 3:1 (large text) using a contrast checker tool.",
            severity=Severity.MAJOR,
        )
    except Exception:
        return Finding(
            criterion="Text contrast ratio (WCAG 1.4.3)",
            status=Status.WARNING,
            detail="Could not analyze banner contrast — banner may be in an iframe. Manual verification needed.",
            severity=Severity.MAJOR,
        )


async def _check_target_size(page: Page, banner_locator) -> Finding:
    """WCAG-006: Check that interactive targets are at least 24x24 CSS pixels."""
    try:
        targets = await banner_locator.evaluate("""el => {
            const buttons = el.querySelectorAll('button, a, [role="button"], input[type="submit"]');
            const results = [];
            buttons.forEach(btn => {
                const rect = btn.getBoundingClientRect();
                results.push({
                    text: btn.textContent?.trim().substring(0, 30),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height),
                });
            });
            return results;
        }""")

        if not targets:
            return Finding(
                criterion="Target size minimum 24x24px (WCAG 2.5.8)",
                status=Status.WARNING,
                detail="No interactive targets found in banner for size measurement. Banner may be in an iframe.",
                severity=Severity.MAJOR,
            )

        undersized = [t for t in targets if t["width"] < 24 or t["height"] < 24]
        if undersized:
            names = ", ".join(f"'{t['text']}' ({t['width']}x{t['height']}px)" for t in undersized)
            return Finding(
                criterion="Target size minimum 24x24px (WCAG 2.5.8)",
                status=Status.FAIL,
                detail=f"Undersized targets: {names}. Minimum is 24x24 CSS pixels.",
                severity=Severity.MAJOR,
            )
        else:
            sizes = ", ".join(f"'{t['text']}' ({t['width']}x{t['height']}px)" for t in targets)
            return Finding(
                criterion="Target size minimum 24x24px (WCAG 2.5.8)",
                status=Status.PASS,
                detail=f"All {len(targets)} targets meet 24x24px minimum: {sizes}.",
            )
    except Exception:
        return Finding(
            criterion="Target size minimum 24x24px (WCAG 2.5.8)",
            status=Status.WARNING,
            detail="Could not measure target sizes — banner may be in an iframe.",
            severity=Severity.MAJOR,
        )


async def _check_aria_labels(page: Page, banner_locator) -> Finding:
    """WCAG-007: Check for proper ARIA landmark and labels."""
    try:
        aria_data = await banner_locator.evaluate("""el => {
            return {
                role: el.getAttribute('role'),
                ariaLabel: el.getAttribute('aria-label'),
                ariaLabelledBy: el.getAttribute('aria-labelledby'),
                ariaDescribedBy: el.getAttribute('aria-describedby'),
                tagName: el.tagName,
                isIframe: el.tagName === 'IFRAME',
                iframeTitle: el.tagName === 'IFRAME' ? el.getAttribute('title') : null,
                buttons: Array.from(el.querySelectorAll('button, [role="button"]')).map(btn => ({
                    text: btn.textContent?.trim().substring(0, 30),
                    ariaLabel: btn.getAttribute('aria-label'),
                    role: btn.getAttribute('role'),
                }))
            };
        }""")

        issues = []
        passes = []

        if aria_data.get("isIframe"):
            if aria_data.get("iframeTitle"):
                passes.append(f"iframe has title='{aria_data['iframeTitle']}'")
            else:
                issues.append("iframe missing title attribute")
        else:
            if aria_data.get("role") in ("dialog", "alertdialog"):
                passes.append(f"role='{aria_data['role']}'")
            else:
                issues.append("Missing role='dialog' on banner")

            if aria_data.get("ariaLabel") or aria_data.get("ariaLabelledBy"):
                passes.append("Has aria-label/aria-labelledby")
            else:
                issues.append("Missing aria-label or aria-labelledby")

        if issues:
            return Finding(
                criterion="ARIA landmarks and labels (WCAG 4.1.2)",
                status=Status.FAIL,
                detail=f"Issues: {'; '.join(issues)}. " + (f"OK: {'; '.join(passes)}." if passes else ""),
                severity=Severity.MAJOR,
            )
        else:
            return Finding(
                criterion="ARIA landmarks and labels (WCAG 4.1.2)",
                status=Status.PASS,
                detail=f"Banner has proper ARIA attributes: {'; '.join(passes)}.",
            )
    except Exception:
        return Finding(
            criterion="ARIA landmarks and labels (WCAG 4.1.2)",
            status=Status.WARNING,
            detail="Could not inspect ARIA attributes — banner may be in an iframe.",
            severity=Severity.MAJOR,
        )


async def _check_lang_attribute(page: Page, banner_locator) -> Finding:
    """WCAG-010: Check banner language matches page lang."""
    try:
        lang_data = await page.evaluate("""() => {
            const html = document.documentElement;
            return {
                pageLang: html.getAttribute('lang'),
            };
        }""")

        banner_lang = await banner_locator.evaluate("el => el.getAttribute('lang') || el.closest('[lang]')?.getAttribute('lang')")

        page_lang = lang_data.get("pageLang")

        if not page_lang:
            return Finding(
                criterion="Banner language (WCAG 3.1.1)",
                status=Status.FAIL,
                detail="Page is missing lang attribute on <html>. Screen readers cannot determine the language.",
                severity=Severity.MINOR,
            )

        if banner_lang and banner_lang != page_lang:
            return Finding(
                criterion="Banner language (WCAG 3.1.1)",
                status=Status.PASS,
                detail=f"Banner has its own lang='{banner_lang}' (page lang='{page_lang}').",
            )

        return Finding(
            criterion="Banner language (WCAG 3.1.1)",
            status=Status.PASS,
            detail=f"Page lang='{page_lang}' applies to banner content.",
        )
    except Exception:
        return Finding(
            criterion="Banner language (WCAG 3.1.1)",
            status=Status.WARNING,
            detail="Could not verify language attributes.",
            severity=Severity.MINOR,
        )


async def _check_preconsent_cookies(cookies_before: list, check: ComplianceCheck) -> Finding:
    """GDPR-001, EPRIV-001, ICO-001: Check for tracking cookies before consent."""
    tracking = [c for c in cookies_before if is_tracking_cookie(c)]
    if tracking:
        names = ", ".join(c.name for c in tracking)
        return Finding(
            criterion=f"{check.title} ({check.id})",
            status=Status.FAIL,
            detail=f"Tracking cookies set before consent: {names}.",
            severity=Severity.CRITICAL,
        )
    return Finding(
        criterion=f"{check.title} ({check.id})",
        status=Status.PASS,
        detail="No tracking cookies detected before consent.",
    )


async def _check_third_party_cookies(cookies: list, url: str, check: ComplianceCheck) -> Finding:
    """EPRIV-004, ICO-006: Check third-party cookie disclosure."""
    page_domain = url.split("//")[-1].split("/")[0]
    base = ".".join(page_domain.split(".")[-2:])
    third_party = [c for c in cookies if base not in c.domain]
    if third_party:
        domains = sorted(set(c.domain for c in third_party))
        return Finding(
            criterion=f"{check.title} ({check.id})",
            status=Status.WARNING,
            detail=f"Third-party cookies from: {', '.join(domains)}. Verify these are disclosed in the cookie policy.",
            severity=Severity.MAJOR,
        )
    return Finding(
        criterion=f"{check.title} ({check.id})",
        status=Status.PASS,
        detail="No third-party cookies detected.",
    )


async def _check_reject_button(banner: BannerDetection, check: ComplianceCheck) -> Finding:
    """CNIL-001: Check reject button is present and equally prominent."""
    reject_keywords = ["reject", "decline", "deny", "refuse", "no thanks"]
    has_reject = any(any(kw in b.lower() for kw in reject_keywords) for b in banner.buttons)
    if not banner.buttons:
        return Finding(
            criterion=f"{check.title} ({check.id})",
            status=Status.WARNING,
            detail="No buttons detected — banner may be in an iframe. Manual verification needed.",
            severity=Severity.CRITICAL,
        )
    if has_reject:
        return Finding(
            criterion=f"{check.title} ({check.id})",
            status=Status.PASS,
            detail=f"Reject button found. Buttons: {', '.join(banner.buttons)}.",
        )
    return Finding(
        criterion=f"{check.title} ({check.id})",
        status=Status.FAIL,
        detail=f"No reject button detected. Buttons found: {', '.join(banner.buttons)}.",
        severity=Severity.CRITICAL,
    )


async def run_automated_checks(
    page: Page,
    context: BrowserContext,
    url: str,
    banner: BannerDetection,
    cookie_audit: CookieAudit,
    frameworks: list[str] | None = None,
) -> list[Finding]:
    """Run all automatable checks for the selected frameworks.

    Returns a list of Finding objects to merge into the report.
    """
    if frameworks is None:
        frameworks = list(ALL_FRAMEWORKS.keys())

    # Collect automatable checks for selected frameworks
    checks = []
    for fw in frameworks:
        fw_checks = ALL_FRAMEWORKS.get(fw, [])
        checks.extend(c for c in fw_checks if c.automated)

    if not checks:
        return []

    findings: list[Finding] = []
    banner_locator = await _find_banner_element(page) if banner.banner_found else None

    for check in checks:
        finding = None

        # Route to the right checker
        if check.id in ("GDPR-001", "EPRIV-001", "ICO-001"):
            finding = await _check_preconsent_cookies(cookie_audit.cookies_before_consent, check)
        elif check.id in ("EPRIV-004", "ICO-006"):
            all_cookies = cookie_audit.cookies_before_consent + cookie_audit.cookies_after_accept
            finding = await _check_third_party_cookies(all_cookies, url, check)
        elif check.id == "CNIL-001":
            finding = await _check_reject_button(banner, check)
        elif check.id == "WCAG-001" and banner_locator:
            finding = await _check_keyboard_accessible(page, banner_locator)
        elif check.id == "WCAG-002":
            finding = await _check_focus_on_load(page)
        elif check.id == "WCAG-005" and banner_locator:
            finding = await _check_contrast(page, banner_locator)
        elif check.id == "WCAG-006" and banner_locator:
            finding = await _check_target_size(page, banner_locator)
        elif check.id == "WCAG-007" and banner_locator:
            finding = await _check_aria_labels(page, banner_locator)
        elif check.id == "WCAG-010" and banner_locator:
            finding = await _check_lang_attribute(page, banner_locator)
        elif banner_locator is None and check.id.startswith("WCAG"):
            finding = Finding(
                criterion=f"{check.title} ({check.id})",
                status=Status.WARNING,
                detail="No banner element accessible for automated check — banner may be in an iframe.",
                severity=Severity.MAJOR,
            )

        if finding is not None:
            # Tag with framework and rule ID
            finding.framework = check.framework
            finding.rule_id = check.id
            findings.append(finding)

    return findings
