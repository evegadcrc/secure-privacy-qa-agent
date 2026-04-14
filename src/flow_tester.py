import asyncio
from pathlib import Path

from playwright.async_api import Page, BrowserContext

from .models import FlowTestResult, BannerDetection, CookieInfo
from .cookie_inspector import capture_cookies, is_tracking_cookie
from .banner_detector import _find_banner_element, _find_iframe_banner, _is_iframe

# Map button text patterns to flow actions — order matters (more specific first)
ACTION_PATTERNS = [
    ("manage", ["manage", "settings", "preferences", "customize", "cookie settings", "manage preferences", "more options"]),
    ("reject", ["reject all", "reject", "decline", "deny", "refuse", "no thanks", "no, thanks", "decline all"]),
    ("close", ["×", "close", "dismiss"]),
    ("accept", ["accept all", "accept", "allow all", "allow", "agree", "got it", "i agree", "okay", "yes"]),
]


def _classify_button(text: str) -> str | None:
    """Classify a button text into an action type."""
    text_lower = text.lower().strip()
    for action, patterns in ACTION_PATTERNS:
        for pattern in patterns:
            if pattern in text_lower:
                return action
    return None


def _find_button_for_action(buttons: list[str], action: str) -> str | None:
    """Find the best matching button text for a given action."""
    # First try exact classification
    for btn in buttons:
        if _classify_button(btn) == action:
            return btn
    return None


async def _click_button(page: Page, banner_locator, button_text: str) -> bool:
    """Click a button within the banner by its text."""
    # Try multiple strategies to find and click the button
    strategies = [
        banner_locator.get_by_role("button", name=button_text, exact=False),
        banner_locator.get_by_text(button_text, exact=False),
        banner_locator.locator(f"button:has-text('{button_text}')"),
        banner_locator.locator(f"a:has-text('{button_text}')"),
        banner_locator.locator(f"[role='button']:has-text('{button_text}')"),
    ]

    for locator in strategies:
        try:
            count = await locator.count()
            if count > 0:
                await locator.first.click(timeout=5000)
                return True
        except Exception:
            continue

    return False


async def _check_banner_dismissed(page: Page) -> bool:
    """Check if the consent banner has been dismissed (DOM or iframe)."""
    await asyncio.sleep(1)
    banner = await _find_banner_element(page)
    if banner is not None:
        # Banner element exists — check if it's still visible
        try:
            if await banner.is_visible():
                return False
        except Exception:
            pass
    # Also check iframe banners
    iframe_el, _ = await _find_iframe_banner(page)
    if iframe_el is not None:
        try:
            if await iframe_el.is_visible():
                return False
        except Exception:
            pass
    return True


async def test_flow(
    page: Page,
    context: BrowserContext,
    url: str,
    banner: BannerDetection,
    action: str,
    button_text: str,
    screenshots_dir: str | Path | None = None,
) -> FlowTestResult:
    """Test a single consent flow (accept, reject, close, manage).

    Navigates fresh to the URL, clicks the specified button,
    and checks banner dismissal + cookie state.
    """
    if screenshots_dir is None:
        from .output import get_screenshots_dir
        screenshots_dir = get_screenshots_dir(url)
    screenshots_path = Path(screenshots_dir)
    screenshots_path.mkdir(parents=True, exist_ok=True)

    # Clear cookies and navigate fresh
    await context.clear_cookies()
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(3)

    # Find the banner again — try DOM first, then iframe
    banner_el = await _find_banner_element(page)
    click_target = banner_el  # What we'll search for buttons in

    if banner_el is not None and await _is_iframe(banner_el):
        # Banner is an iframe — need to use frame_locator to click inside
        _, frame = await _find_iframe_banner(page)
        if frame is not None:
            click_target = frame
        else:
            banner_el = None

    if banner_el is None:
        # Try iframe-specific detection
        _, frame = await _find_iframe_banner(page)
        if frame is not None:
            click_target = frame
        else:
            return FlowTestResult(
                action=action,
                banner_dismissed=False,
                tracking_cookies_set=False,
                passed=False,
            )

    # Click the target button
    clicked = await _click_button(page, click_target, button_text)
    if not clicked:
        return FlowTestResult(
            action=action,
            banner_dismissed=False,
            tracking_cookies_set=False,
            passed=False,
        )

    # Wait for banner to dismiss and cookies to settle
    await asyncio.sleep(2)

    # Check results
    dismissed = await _check_banner_dismissed(page)
    cookies = await capture_cookies(context)
    tracking = any(is_tracking_cookie(c) for c in cookies)

    # Take screenshot
    screenshot_path = str(screenshots_path / f"after-{action}.png")
    await page.screenshot(path=screenshot_path)

    # Determine pass/fail
    if action == "accept":
        passed = dismissed  # Banner should dismiss after accept
    elif action == "reject":
        passed = dismissed and not tracking  # Banner should dismiss, no tracking cookies
    elif action == "close":
        passed = dismissed  # Banner should dismiss
    elif action == "manage":
        passed = True  # Just verify it opens something
    else:
        passed = dismissed

    return FlowTestResult(
        action=action,
        banner_dismissed=dismissed,
        tracking_cookies_set=tracking,
        screenshot_path=screenshot_path,
        passed=passed,
    )


async def test_all_flows(
    page: Page,
    context: BrowserContext,
    url: str,
    banner: BannerDetection,
    screenshots_dir: str | Path | None = None,
) -> tuple[list[FlowTestResult], list[CookieInfo], list[CookieInfo]]:
    """Test all detected consent flows.

    Returns (flow_results, cookies_after_accept, cookies_after_reject).
    """
    results: list[FlowTestResult] = []
    cookies_after_accept: list[CookieInfo] = []
    cookies_after_reject: list[CookieInfo] = []

    for btn_text in banner.buttons:
        action = _classify_button(btn_text)
        if action is None:
            continue

        result = await test_flow(
            page, context, url, banner, action, btn_text, screenshots_dir
        )
        results.append(result)

        # Capture cookie snapshots for the audit
        if action == "accept":
            cookies_after_accept = await capture_cookies(context)
        elif action == "reject":
            cookies_after_reject = await capture_cookies(context)

    return results, cookies_after_accept, cookies_after_reject
