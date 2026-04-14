import asyncio
import os
from pathlib import Path

import click
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .banner_detector import detect_banner
from .cookie_inspector import capture_cookies, audit_cookies
from .flow_tester import test_all_flows
from .ai_analyzer import analyze_compliance, export_for_llm, parse_analysis_result
from .report_generator import generate_report, generate_html_report
from .output import get_output_dir, get_screenshots_dir
from .models import ComplianceReport, Status

load_dotenv()

console = Console()


# ---------------------------------------------------------------------------
# CLI group
# ---------------------------------------------------------------------------
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Cookie Consent Compliance QA Agent.

    Run 'audit' for automated scanning, 'assisted' for guided manual testing,
    or 'generate-tests' to create an Excel test plan.

    \b
    Examples:
      python -m src.main audit https://example.com
      python -m src.main assisted https://example.com
      python -m src.main generate-tests https://example.com
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# ---------------------------------------------------------------------------
# audit — automated scan
# ---------------------------------------------------------------------------
async def run_audit(
    url: str,
    output: str | None,
    headless: bool,
    verbose: bool,
    analysis_file: str | None,
    frameworks: list[str] | None = None,
) -> None:
    """Run the full cookie consent compliance audit."""
    site_dir = get_output_dir(url)
    screenshots_dir = get_screenshots_dir(url)

    if verbose:
        console.print(f"  [dim]Output directory: {site_dir}[/dim]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:

        task = progress.add_task("Launching browser...", total=None)
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 720},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = await context.new_page()

            progress.update(task, description="Navigating and capturing pre-consent cookies...")
            await page.goto(url, wait_until="domcontentloaded")
            await asyncio.sleep(2)
            cookies_before = await capture_cookies(context)

            if verbose:
                console.print(f"  [dim]Found {len(cookies_before)} cookies before consent[/dim]")

            progress.update(task, description="Detecting consent banner...")
            await context.clear_cookies()
            banner = await detect_banner(page, url, screenshots_dir)

            if banner.banner_found:
                console.print(
                    Panel(
                        f"[bold green]Banner detected![/bold green]\n"
                        f"Buttons: {', '.join(banner.buttons) or 'None identified'}\n"
                        f"Text preview: {(banner.text or '')[:200]}...",
                        title="Banner Detection",
                    )
                )
            else:
                console.print("[bold yellow]No consent banner detected.[/bold yellow]")
                if frameworks:
                    console.print(
                        Panel(
                            "[bold yellow]No banner found — framework checks that inspect the banner will be inconclusive.[/bold yellow]\n\n"
                            "You can still:\n"
                            f"  1. Run without -f to get the full AI analysis:\n"
                            f"     [dim]python -m src.main audit {url}[/dim]\n"
                            f"  2. Use assisted mode to manually verify:\n"
                            f"     [dim]python -m src.main assisted {url} -f {','.join(frameworks)}[/dim]\n"
                            f"  3. Generate test cases for manual QA:\n"
                            f"     [dim]python -m src.main generate-tests {url} -f {','.join(frameworks)}[/dim]",
                            title="Next Steps",
                            border_style="yellow",
                        )
                    )

            cookies_before = await capture_cookies(context)

            progress.update(task, description="Testing consent flows...")
            flow_results = []
            cookies_after_accept = []
            cookies_after_reject = []

            if banner.banner_found and banner.buttons:
                flow_results, cookies_after_accept, cookies_after_reject = await test_all_flows(
                    page, context, url, banner, screenshots_dir
                )
                if verbose:
                    for fr in flow_results:
                        status = "[green]PASS[/green]" if fr.passed else "[red]FAIL[/red]"
                        console.print(f"  [dim]Flow '{fr.action}': {status}[/dim]")

            progress.update(task, description="Analyzing cookie behavior...")
            cookie_audit = await audit_cookies(
                context,
                cookies_before=cookies_before,
                cookies_after_accept=cookies_after_accept,
                cookies_after_reject=cookies_after_reject,
            )

            if verbose and cookie_audit.violations:
                for v in cookie_audit.violations:
                    console.print(f"  [dim red]Violation: {v}[/dim red]")

            # Run automated framework checks — always runs (all frameworks by default, -f to filter)
            from .utils.automated_checks import run_automated_checks
            fw_to_run = frameworks  # None means all
            fw_label = ", ".join(frameworks) if frameworks else "all"
            framework_findings = []
            no_banner_skip = False

            if banner.banner_found:
                progress.update(task, description=f"Running automated checks ({fw_label})...")
                framework_findings = await run_automated_checks(
                    page, context, url, banner, cookie_audit, fw_to_run
                )
                if verbose:
                    for f in framework_findings:
                        style = {"pass": "green", "fail": "red", "warning": "yellow"}.get(f.status.value, "white")
                        console.print(f"  [dim][{style}]{f.status.value.upper()}[/{style}] {f.criterion}[/dim]")
            else:
                # No banner — run checks that don't need one (cookie checks still work)
                progress.update(task, description=f"Running automated checks ({fw_label})...")
                framework_findings = await run_automated_checks(
                    page, context, url, banner, cookie_audit, fw_to_run
                )
                if verbose:
                    for f in framework_findings:
                        style = {"pass": "green", "fail": "red", "warning": "yellow"}.get(f.status.value, "white")
                        console.print(f"  [dim][{style}]{f.status.value.upper()}[/{style}] {f.criterion}[/dim]")
                # Only flag no_banner_skip if -f was explicitly set and ONLY banner-dependent frameworks
                if frameworks and not framework_findings:
                    no_banner_skip = True

            await browser.close()

        # AI analysis
        findings = []
        overall_score = ""
        summary = ""
        recommendations = []

        if analysis_file:
            progress.update(task, description="Importing analysis from file...")
            try:
                overall_score, findings, summary, recommendations = parse_analysis_result(analysis_file)
            except FileNotFoundError as e:
                progress.stop()
                console.print(Panel(str(e), title="File Not Found", border_style="red"))
                return
        elif os.environ.get("ANTHROPIC_API_KEY"):
            progress.update(task, description="Running AI compliance analysis...")
            overall_score, findings, summary, recommendations = analyze_compliance(
                banner, cookie_audit
            )
        else:
            progress.update(task, description="Exporting data for LLM analysis...")
            prompt_path = export_for_llm(banner, cookie_audit, url, site_dir)
            analysis_result_path = site_dir / "analysis-result.json"

            console.print()
            console.print(
                Panel(
                    "[bold yellow]No ANTHROPIC_API_KEY found.[/bold yellow]\n\n"
                    "Two ways to get the AI analysis:\n\n"
                    f"[bold]1. Paste the prompt into any LLM:[/bold]\n"
                    f"   File: [cyan]{prompt_path}[/cyan]\n"
                    f"   Save the JSON response as [cyan]{analysis_result_path}[/cyan], then re-run:\n"
                    f"   [dim]python -m src.main audit {url} --analysis {analysis_result_path}[/dim]\n\n"
                    f"[bold]2. In Claude Code:[/bold]\n"
                    f"   Ask Claude to read [cyan]{site_dir / 'analysis-input.json'}[/cyan] and analyze it.",
                    title="AI Analysis — Export Mode",
                    border_style="yellow",
                )
            )

            overall_score, findings, summary, recommendations = (
                "pending",
                [],
                "AI analysis pending — data exported for external LLM analysis.",
                [
                    f"Step 1: Paste the prompt from {prompt_path} into any LLM (ChatGPT, Claude, Gemini).",
                    f"Step 2: Save the JSON response as {analysis_result_path}",
                    f"Step 3: Re-run: python -m src.main audit {url} --analysis {analysis_result_path}",
                ],
            )

        progress.update(task, description="Generating report...")

        # Merge findings: AI analysis + framework automated checks
        all_findings = findings + framework_findings

        # Derive overall score from all findings if AI analysis didn't provide one
        if overall_score in ("", "pending") and all_findings:
            passed = sum(1 for f in all_findings if f.status == Status.PASS)
            failed = sum(1 for f in all_findings if f.status == Status.FAIL)
            warnings = sum(1 for f in all_findings if f.status == Status.WARNING)
            total = len(all_findings)
            if passed == 0 and failed == 0:
                overall_score = "partial"
            elif failed == 0 and warnings == 0:
                overall_score = "pass"
            elif failed == 0:
                overall_score = "partial"
            elif passed > failed:
                overall_score = "partial"
            else:
                overall_score = "fail"
            if not summary:
                summary = f"Automated checks: {passed}/{total} passed, {failed} failed, {warnings} warnings."

        report = ComplianceReport(
            url=url,
            overall_score=overall_score,
            findings=all_findings,
            cookie_audit=cookie_audit,
            flow_results=flow_results,
            summary=summary,
            recommendations=recommendations,
        )

        markdown = generate_report(report)
        progress.update(task, description="Done!", completed=True)

    # Save reports — default to output/{domain}/
    if output is None:
        output = str(site_dir / "report.md")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    Path(output).write_text(markdown)

    html = generate_html_report(report)
    html_path = Path(output).with_suffix(".html")
    html_path.write_text(html)

    # Summary
    passed = sum(1 for f in all_findings if f.status == Status.PASS)
    failed = sum(1 for f in all_findings if f.status == Status.FAIL)
    warnings = sum(1 for f in all_findings if f.status == Status.WARNING)
    total = len(all_findings)

    console.print()
    console.print(
        Panel(
            f"[bold]Score: {report.overall_score.upper()}[/bold] — "
            f"{passed} passed, {failed} failed, {warnings} warnings ({total} checks)\n\n"
            f"Reports generated:\n"
            f"  [cyan]{output}[/cyan]\n"
            f"  [cyan]{html_path}[/cyan]",
            title="Done",
            border_style="green",
        )
    )


@cli.command()
@click.argument("url")
@click.option("--output", "-o", default=None, help="Save report to file (default: output/{domain}/report.md)")
@click.option("--headless/--headed", default=True, help="Run browser in headless mode")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed steps")
@click.option("--analysis", "-a", default=None, help="Import analysis from a JSON file (skip API call)")
@click.option("--frameworks", "-f", default=None, help="Run automated framework checks (e.g. WCAG, GDPR,WCAG). Default: none.")
def audit(url: str, output: str | None, headless: bool, verbose: bool, analysis: str | None, frameworks: str | None) -> None:
    """Run automated compliance audit on a URL.

    \b
    Examples:
      python -m src.main audit https://secureprivacy.ai
      python -m src.main audit https://secureprivacy.ai -f WCAG
      python -m src.main audit https://example.com -f GDPR,WCAG,CNIL -v
      python -m src.main audit https://example.com --analysis result.json
    """
    from .trial import check_trial, record_scan, trial_status_message

    # Check demo limit
    allowed, remaining = check_trial()
    if not allowed:
        console.print(Panel(trial_status_message(remaining), title="Demo Limit", border_style="red"))
        return

    fw_list = [fw.strip() for fw in frameworks.split(",")] if frameworks else None

    fw_label = f"\nFrameworks: {', '.join(fw_list)}" if fw_list else ""
    console.print(
        Panel(
            f"[bold]Cookie Consent Compliance Audit[/bold]\n"
            f"Target: {url}{fw_label}",
            border_style="blue",
        )
    )
    console.print(trial_status_message(remaining))

    asyncio.run(run_audit(url, output, headless, verbose, analysis, fw_list))

    # Record scan after successful completion
    record_scan()


# ---------------------------------------------------------------------------
# assisted — interactive guided manual testing
# ---------------------------------------------------------------------------
@cli.command()
@click.argument("url")
@click.option(
    "--frameworks", "-f", default=None,
    help="Comma-separated frameworks to test (e.g. GDPR,CNIL). Default: all.",
)
@click.option("--output-dir", "-o", default=None, help="Directory for session results (default: output/{domain}/assisted)")
def assisted(url: str, frameworks: str | None, output_dir: str | None) -> None:
    """Interactive Playwright-guided manual compliance testing.

    Opens a headed browser and walks you through each compliance check
    step-by-step, capturing browser state and recording your results.

    \b
    Frameworks: GDPR, ePrivacy, EDPB, Planet49, CNIL, ICO, WCAG

    \b
    Examples:
      python -m src.main assisted https://secureprivacy.ai
      python -m src.main assisted https://example.com -f GDPR,CNIL
    """
    from .utils.assisted_testing import run_assisted_testing

    fw_list = [fw.strip() for fw in frameworks.split(",")] if frameworks else None

    if output_dir is None:
        output_dir = str(get_output_dir(url) / "assisted")

    console.print(
        Panel(
            f"[bold]Assisted Compliance Testing[/bold]\n"
            f"Target: {url}\n"
            f"Frameworks: {frameworks or 'All (GDPR, ePrivacy, EDPB, Planet49, CNIL, ICO, WCAG)'}",
            border_style="green",
        )
    )
    asyncio.run(run_assisted_testing(url, fw_list, output_dir))


# ---------------------------------------------------------------------------
# generate-tests — Excel test case generator
# ---------------------------------------------------------------------------
@cli.command("generate-tests")
@click.argument("url")
@click.option(
    "--frameworks", "-f", default=None,
    help="Comma-separated frameworks (e.g. GDPR,CNIL). Default: all.",
)
@click.option("--output", "-o", default=None, help="Output Excel file path (default: output/{domain}/compliance-tests.xlsx)")
def generate_tests(url: str, frameworks: str | None, output: str | None) -> None:
    """Generate an Excel workbook of manual compliance test cases.

    Scans the site to gather context (banner, cookies), then generates
    tailored test cases organized by compliance framework.

    \b
    Frameworks: GDPR, ePrivacy, EDPB, Planet49, CNIL, ICO, WCAG

    \b
    Examples:
      python -m src.main generate-tests https://secureprivacy.ai
      python -m src.main generate-tests https://example.com -f GDPR,ICO -o tests.xlsx
    """
    from .utils.test_case_generator import generate_test_cases

    fw_list = [fw.strip() for fw in frameworks.split(",")] if frameworks else None

    if output is None:
        output = str(get_output_dir(url) / "compliance-tests.xlsx")

    console.print(
        Panel(
            f"[bold]Compliance Test Case Generator[/bold]\n"
            f"Target: {url}\n"
            f"Frameworks: {frameworks or 'All (GDPR, ePrivacy, EDPB, Planet49, CNIL, ICO, WCAG)'}",
            border_style="magenta",
        )
    )
    asyncio.run(generate_test_cases(url, fw_list, output))


# ---------------------------------------------------------------------------
# wcag-scan — full page WCAG 2.2 AA accessibility scan
# ---------------------------------------------------------------------------
@cli.command("wcag-scan")
@click.argument("url")
@click.option("--pages", "-p", multiple=True, help="Additional page paths to scan (repeatable, or comma-separated)")
@click.option("--headless/--headed", default=True, help="Run browser in headless mode")
@click.option("--output-dir", "-o", default=None, help="Output directory (default: output/{domain}/)")
def wcag_scan(url: str, pages: tuple, headless: bool, output_dir: str | None) -> None:
    """Full-page WCAG 2.2 AA accessibility scan using axe-core.

    Scans the entire page (not just the consent banner) against WCAG 2.2
    Level AA criteria. Uses axe-core, the industry-standard accessibility
    testing engine.

    \b
    Examples:
      python -m src.main wcag-scan https://secureprivacy.ai
      python -m src.main wcag-scan https://example.com -p /about -p /contact
      python -m src.main wcag-scan https://example.com -p /about,/contact,/pricing
      python -m src.main wcag-scan https://example.com --headed
    """
    from .utils.wcag_scanner import run_wcag_scan

    # Support both: -p /a -p /b and -p /a,/b
    page_list = []
    for p in pages:
        page_list.extend(part.strip() for part in p.split(",") if part.strip())
    page_list = page_list or None

    console.print(
        Panel(
            f"[bold]WCAG 2.2 AA Full-Page Accessibility Scan[/bold]\n"
            f"Target: {url}"
            + (f"\nAdditional pages: {', '.join(page_list)}" if page_list else ""),
            border_style="magenta",
        )
    )
    asyncio.run(run_wcag_scan(url, page_list, headless, output_dir))


if __name__ == "__main__":
    cli()
