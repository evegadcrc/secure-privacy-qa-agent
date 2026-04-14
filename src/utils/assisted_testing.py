"""Interactive Playwright-assisted manual compliance testing.

Opens a headed browser (like playwright codegen) and walks the user through
each compliance check step-by-step, capturing state and recording results.

Usage:
    python -m src.main assisted https://example.com
    python -m src.main assisted https://example.com --frameworks GDPR,CNIL
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page, BrowserContext
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich.rule import Rule

from ..cookie_inspector import capture_cookies, classify_cookie
from ..banner_detector import _find_banner_element
from .compliance_frameworks import (
    ComplianceCheck,
    ALL_CHECKS,
    ALL_FRAMEWORKS,
    get_checks_by_framework,
)

console = Console()

RESULT_CHOICES = {"p": "pass", "f": "fail", "w": "warning", "s": "skip", "n/a": "n/a"}

# Return value from _prompt_between_checks
CONTINUE = "continue"
SKIP_FRAMEWORK = "skip_framework"
FINISH = "finish"


def _severity_style(severity: str) -> str:
    if severity == "critical":
        return "bold red"
    elif severity == "major":
        return "yellow"
    return "dim"


async def _capture_state_snapshot(page: Page, context: BrowserContext, screenshots_dir: Path, check_id: str) -> dict:
    """Capture current browser state: cookies, URL, screenshot."""
    cookies = await capture_cookies(context)
    screenshot_path = screenshots_dir / f"{check_id}.png"
    try:
        await page.screenshot(path=str(screenshot_path))
    except Exception:
        screenshot_path = None

    return {
        "url": page.url,
        "cookies": [c.model_dump() for c in cookies],
        "cookie_count": len(cookies),
        "tracking_cookies": [c.name for c in cookies if c.category in ("analytics", "marketing")],
        "screenshot": str(screenshot_path) if screenshot_path else None,
    }


def _print_check_header(check: ComplianceCheck, index: int, total: int) -> None:
    """Print the check header with framework, title, and severity."""
    console.print()
    console.print(Rule(f"Check {index}/{total}"))
    console.print(
        Panel(
            f"[bold]{check.title}[/bold]\n"
            f"[dim]{check.description}[/dim]\n\n"
            f"[{_severity_style(check.severity)}]Severity: {check.severity.upper()}[/{_severity_style(check.severity)}]"
            f"  |  Reference: [dim]{check.references}[/dim]",
            title=f"[cyan]{check.framework}[/cyan] — {check.id}",
            border_style="cyan",
        )
    )


def _print_steps(check: ComplianceCheck) -> None:
    """Print the test steps for the user to follow."""
    console.print("\n[bold]Steps to execute:[/bold]")
    for i, step in enumerate(check.steps, 1):
        console.print(f"  [cyan]{i}.[/cyan] {step}")
    console.print(f"\n[bold]Expected result:[/bold] [green]{check.expected}[/green]")


def _print_state_snapshot(snapshot: dict) -> None:
    """Print a summary of the captured browser state."""
    console.print(f"\n  [dim]Current URL: {snapshot['url']}[/dim]")
    console.print(f"  [dim]Total cookies: {snapshot['cookie_count']}[/dim]")
    if snapshot["tracking_cookies"]:
        console.print(f"  [red]Tracking cookies found: {', '.join(snapshot['tracking_cookies'])}[/red]")
    else:
        console.print(f"  [green]No tracking cookies detected[/green]")
    if snapshot["screenshot"]:
        console.print(f"  [dim]Screenshot saved: {snapshot['screenshot']}[/dim]")


def _prompt_result() -> tuple[str, str]:
    """Prompt the user for the check result and optional notes."""
    console.print()
    console.print("[bold]Record your result:[/bold]")
    console.print("  [green]p[/green]=Pass  [red]f[/red]=Fail  [yellow]w[/yellow]=Warning  [dim]s[/dim]=Skip  [dim]n/a[/dim]=Not Applicable")

    result = Prompt.ask(
        "Result",
        choices=list(RESULT_CHOICES.keys()),
        default="s",
    )
    notes = Prompt.ask("Notes (optional)", default="")

    return RESULT_CHOICES[result], notes


async def _run_automated_precheck(
    page: Page, context: BrowserContext, check: ComplianceCheck
) -> str | None:
    """Run automated pre-check if available. Returns a hint string or None."""
    if not check.automated:
        return None

    hints = []
    cookies = await capture_cookies(context)

    if "pre-consent" in check.id.lower() or "prior consent" in check.title.lower() or "GDPR-001" == check.id or "EPRIV-001" == check.id:
        tracking = [c for c in cookies if c.category in ("analytics", "marketing")]
        if tracking:
            names = ", ".join(c.name for c in tracking)
            hints.append(f"[red]AUTO-DETECT: {len(tracking)} tracking cookie(s) found before consent: {names}[/red]")
        else:
            hints.append("[green]AUTO-DETECT: No tracking cookies found before consent.[/green]")

    if "reject" in check.title.lower() or "CNIL-001" == check.id:
        banner = await _find_banner_element(page)
        if banner:
            from ..banner_detector import _extract_buttons
            buttons = await _extract_buttons(banner)
            reject_keywords = ["reject", "decline", "deny", "refuse", "no thanks"]
            has_reject = any(
                any(kw in btn.lower() for kw in reject_keywords) for btn in buttons
            )
            if has_reject:
                hints.append(f"[green]AUTO-DETECT: Reject button found. Buttons: {', '.join(buttons)}[/green]")
            else:
                hints.append(f"[red]AUTO-DETECT: No reject button detected. Buttons found: {', '.join(buttons) or 'None (iframe?)'}[/red]")

    if "third-party" in check.title.lower() or "third party" in check.title.lower():
        page_domain = page.url.split("//")[-1].split("/")[0].split(".")[-2]
        third_party = [c for c in cookies if page_domain not in c.domain]
        if third_party:
            domains = set(c.domain for c in third_party)
            hints.append(f"[yellow]AUTO-DETECT: Third-party cookies from: {', '.join(domains)}[/yellow]")
        else:
            hints.append("[green]AUTO-DETECT: No third-party cookies detected.[/green]")

    if hints:
        return "\n".join(hints)
    return None


async def run_assisted_testing(
    url: str,
    frameworks: list[str] | None = None,
    output_dir: str = "assisted-results",
) -> None:
    """Run the interactive assisted testing session."""

    # Select checks
    if frameworks:
        checks = []
        for fw in frameworks:
            fw_checks = get_checks_by_framework(fw)
            if not fw_checks:
                console.print(f"[yellow]Unknown framework: {fw}. Available: {', '.join(ALL_FRAMEWORKS.keys())}[/yellow]")
            checks.extend(fw_checks)
    else:
        checks = ALL_CHECKS

    if not checks:
        console.print("[red]No checks selected. Exiting.[/red]")
        return

    total = len(checks)
    results_dir = Path(output_dir)
    screenshots_dir = results_dir / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Session header
    console.print(
        Panel(
            f"[bold]Assisted Compliance Testing Session[/bold]\n\n"
            f"URL: [cyan]{url}[/cyan]\n"
            f"Checks: {total} across {len(set(c.framework for c in checks))} framework(s)\n"
            f"Frameworks: {', '.join(sorted(set(c.framework for c in checks)))}\n\n"
            f"[dim]The browser will open in headed mode.\n"
            f"Follow the steps for each check and record your result.\n"
            f"Press Ctrl+C at any time to end the session early (results will be saved).[/dim]",
            title="Assisted Testing",
            border_style="blue",
        )
    )

    if not Confirm.ask("Ready to begin?", default=True):
        return

    session_results: list[dict] = []
    session_start = datetime.now()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()

        # Initial navigation
        console.print(f"\n[dim]Navigating to {url}...[/dim]")
        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        current_framework = None
        idx = 0

        try:
            while idx < total:
                check = checks[idx]
                check_num = idx + 1

                # Print framework separator when switching
                if check.framework != current_framework:
                    current_framework = check.framework
                    console.print()
                    console.print(Rule(f"[bold blue]{current_framework}[/bold blue]", style="blue"))

                _print_check_header(check, check_num, total)
                _print_steps(check)

                # Run automated pre-check if available
                auto_hint = await _run_automated_precheck(page, context, check)
                if auto_hint:
                    console.print(f"\n{auto_hint}")

                # Capture state
                console.print("\n[dim]Capturing browser state...[/dim]")
                snapshot = await _capture_state_snapshot(page, context, screenshots_dir, check.id)
                _print_state_snapshot(snapshot)

                # User interaction prompt
                console.print()
                console.print("[bold]Ready?[/bold]")
                console.print("  [green]y[/green] = Interact with browser, then record result")
                console.print("  [dim]n[/dim] = Record result now (no browser interaction needed)")
                console.print("  [dim]s[/dim] = Skip this check")
                console.print(f"  [red]f[/red] = Finish session (save {len(session_results)} results collected)")

                action = Prompt.ask("Action", choices=["y", "n", "s", "f"], default="y")

                if action == "f":
                    console.print("\n[yellow]Finishing session. Saving results...[/yellow]")
                    break

                if action == "s":
                    session_results.append({
                        "check_id": check.id,
                        "framework": check.framework,
                        "category": check.category,
                        "title": check.title,
                        "severity": check.severity,
                        "result": "skip",
                        "notes": "Skipped by user",
                        "snapshot": snapshot,
                        "timestamp": datetime.now().isoformat(),
                    })
                    console.print(f"[dim]Skipped: {check.id}[/dim]")
                    idx += 1
                    continue

                if action == "y":
                    console.print("[dim]Interact with the browser now. Press Enter when ready to record...[/dim]")
                    Prompt.ask("", default="")
                    # Re-capture after interaction
                    snapshot = await _capture_state_snapshot(page, context, screenshots_dir, f"{check.id}-after")
                    console.print("[dim]Updated state after interaction:[/dim]")
                    _print_state_snapshot(snapshot)

                # Record result (action == "y" or "n")
                result, notes = _prompt_result()

                session_results.append({
                    "check_id": check.id,
                    "framework": check.framework,
                    "category": check.category,
                    "title": check.title,
                    "severity": check.severity,
                    "result": result,
                    "notes": notes,
                    "snapshot": snapshot,
                    "timestamp": datetime.now().isoformat(),
                })

                status_style = {
                    "pass": "green", "fail": "red", "warning": "yellow",
                    "skip": "dim", "n/a": "dim",
                }
                console.print(
                    f"\n[{status_style.get(result, 'white')}]Recorded: {check.id} — {result.upper()}[/{status_style.get(result, 'white')}]"
                )

                idx += 1

                # Between checks: show progress and offer continue / skip framework / finish
                if idx < total:
                    next_check = checks[idx]
                    remaining_in_fw = sum(1 for c in checks[idx:] if c.framework == check.framework)

                    console.print()
                    console.print(f"  [dim]Progress: {idx}/{total} completed  |  "
                                  f"Next: {next_check.id} ({next_check.framework})[/dim]")

                    choices = ["c", "f"]
                    console.print()
                    console.print("  [green]c[/green] = Continue to next check")
                    if remaining_in_fw > 0 and next_check.framework == check.framework:
                        console.print(f"  [yellow]s[/yellow] = Skip rest of {check.framework} ({remaining_in_fw} left)")
                        choices.append("s")
                    console.print(f"  [red]f[/red] = Finish session")

                    nav = Prompt.ask("Action", choices=choices, default="c")

                    if nav == "f":
                        console.print("\n[yellow]Finishing session. Saving results...[/yellow]")
                        break
                    elif nav == "s":
                        skip_fw = check.framework
                        skipped = 0
                        while idx < total and checks[idx].framework == skip_fw:
                            session_results.append({
                                "check_id": checks[idx].id,
                                "framework": checks[idx].framework,
                                "category": checks[idx].category,
                                "title": checks[idx].title,
                                "severity": checks[idx].severity,
                                "result": "skip",
                                "notes": f"Skipped (user skipped rest of {skip_fw})",
                                "snapshot": {},
                                "timestamp": datetime.now().isoformat(),
                            })
                            skipped += 1
                            idx += 1
                        console.print(f"[yellow]Skipped {skipped} remaining {skip_fw} checks.[/yellow]")

                    # Clear cookies if next check needs fresh session
                    if idx < total:
                        upcoming = checks[idx]
                        if "fresh" in " ".join(upcoming.steps).lower() or "clear" in " ".join(upcoming.steps).lower():
                            if Confirm.ask("Next check needs a fresh session. Clear cookies and reload?", default=True):
                                await context.clear_cookies()
                                await page.goto(url, wait_until="domcontentloaded")
                                await asyncio.sleep(3)
                                console.print("[dim]Cookies cleared, page reloaded.[/dim]")

        except KeyboardInterrupt:
            console.print("\n\n[yellow]Session interrupted. Saving results collected so far...[/yellow]")

        await browser.close()

    # Save session results
    session_data = {
        "url": url,
        "session_start": session_start.isoformat(),
        "session_end": datetime.now().isoformat(),
        "frameworks": sorted(set(c.framework for c in checks)),
        "total_checks": total,
        "completed": len(session_results),
        "results": session_results,
    }

    results_path = results_dir / "session-results.json"
    results_path.write_text(json.dumps(session_data, indent=2))

    # Print summary
    _print_session_summary(session_results, total, results_path)

    # Generate markdown report
    report_path = results_dir / "assisted-report.md"
    report_path.write_text(_generate_session_report(session_data))
    console.print(f"[green]Report saved to {report_path}[/green]")


def _print_session_summary(results: list[dict], total: int, results_path: Path) -> None:
    """Print a summary table of the session results."""
    console.print()
    console.print(Rule("Session Summary"))

    table = Table(show_header=True, header_style="bold")
    table.add_column("ID", style="cyan")
    table.add_column("Framework")
    table.add_column("Check")
    table.add_column("Severity")
    table.add_column("Result")
    table.add_column("Notes", max_width=40)

    pass_count = fail_count = warn_count = skip_count = 0
    for r in results:
        status = r["result"]
        if status == "pass":
            style = "green"
            pass_count += 1
        elif status == "fail":
            style = "red"
            fail_count += 1
        elif status == "warning":
            style = "yellow"
            warn_count += 1
        else:
            style = "dim"
            skip_count += 1

        table.add_row(
            r["check_id"],
            r["framework"],
            r["title"][:40],
            r["severity"],
            Text(status.upper(), style=style),
            r.get("notes", ""),
        )

    console.print(table)
    console.print(
        f"\n[bold]Results:[/bold] "
        f"[green]{pass_count} passed[/green] | "
        f"[red]{fail_count} failed[/red] | "
        f"[yellow]{warn_count} warnings[/yellow] | "
        f"[dim]{skip_count} skipped[/dim] | "
        f"{total - len(results)} not reached"
    )
    console.print(f"[dim]Full results saved to {results_path}[/dim]")


def _generate_session_report(session: dict) -> str:
    """Generate a markdown report from the session results."""
    lines = [
        "# Assisted Compliance Testing Report\n",
        f"**URL:** {session['url']}",
        f"**Date:** {session['session_start'][:10]}",
        f"**Frameworks:** {', '.join(session['frameworks'])}",
        f"**Checks completed:** {session['completed']}/{session['total_checks']}",
        "",
    ]

    # Summary counts
    results = session["results"]
    pass_count = sum(1 for r in results if r["result"] == "pass")
    fail_count = sum(1 for r in results if r["result"] == "fail")
    warn_count = sum(1 for r in results if r["result"] == "warning")

    lines.append(f"## Summary: {pass_count} passed, {fail_count} failed, {warn_count} warnings\n")

    # Group by framework
    by_framework: dict[str, list[dict]] = {}
    for r in results:
        by_framework.setdefault(r["framework"], []).append(r)

    for fw, fw_results in by_framework.items():
        lines.append(f"## {fw}\n")
        lines.append("| ID | Check | Severity | Result | Notes |")
        lines.append("|----|-------|----------|--------|-------|")
        for r in fw_results:
            lines.append(
                f"| {r['check_id']} | {r['title']} | {r['severity']} | "
                f"{r['result'].upper()} | {r.get('notes', '')} |"
            )
        lines.append("")

    # Critical failures
    critical_fails = [r for r in results if r["result"] == "fail" and r["severity"] == "critical"]
    if critical_fails:
        lines.append("## Critical Failures\n")
        for r in critical_fails:
            lines.append(f"- **{r['check_id']}** ({r['framework']}): {r['title']}")
            if r.get("notes"):
                lines.append(f"  - Notes: {r['notes']}")
            tracking = r.get("snapshot", {}).get("tracking_cookies", [])
            if tracking:
                lines.append(f"  - Tracking cookies: {', '.join(tracking)}")
        lines.append("")

    return "\n".join(lines)
