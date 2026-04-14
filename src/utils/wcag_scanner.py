"""Full-page WCAG 2.2 AA accessibility scan using axe-core.

Injects the axe-core accessibility engine into the page via Playwright,
runs a full audit against WCAG 2.2 Level AA criteria, and generates
structured reports (Markdown + HTML).

This is a standalone page-level scan — separate from the consent banner checks.

Usage:
    python -m src.main wcag-scan https://example.com
    python -m src.main wcag-scan https://example.com --pages /about,/contact
"""

import asyncio
import json
from datetime import date
from pathlib import Path
from urllib.parse import urljoin

from playwright.async_api import async_playwright, Page
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..output import get_output_dir

console = Console()

AXE_CDN_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"

# axe-core tags for WCAG 2.2 AA
AXE_RUN_OPTIONS = {
    "runOnly": {
        "type": "tag",
        "values": ["wcag2a", "wcag2aa", "wcag22aa"],
    },
    "resultTypes": ["violations", "passes", "incomplete"],
}

IMPACT_ORDER = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}


async def _inject_axe(page: Page) -> bool:
    """Inject axe-core into the page. Returns True on success."""
    try:
        await page.add_script_tag(url=AXE_CDN_URL)
        # Wait for axe to be available
        await page.wait_for_function("typeof window.axe !== 'undefined'", timeout=10000)
        return True
    except Exception as e:
        console.print(f"[red]Failed to inject axe-core: {e}[/red]")
        return False


async def _run_axe(page: Page) -> dict:
    """Run axe-core and return the results."""
    results = await page.evaluate(
        """async (options) => {
            const results = await axe.run(document, options);
            return {
                violations: results.violations,
                passes: results.passes,
                incomplete: results.incomplete,
                url: results.url,
                timestamp: results.timestamp,
            };
        }""",
        AXE_RUN_OPTIONS,
    )
    return results


def _impact_style(impact: str) -> str:
    return {"critical": "bold red", "serious": "red", "moderate": "yellow", "minor": "dim"}.get(impact, "white")


def _esc(text: str) -> str:
    """Escape HTML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _format_nodes(nodes: list) -> str:
    """Format affected nodes into readable text."""
    lines = []
    for node in nodes[:5]:  # Limit to first 5 for readability
        target = ", ".join(node.get("target", []))
        html = node.get("html", "")[:120]
        lines.append(f"  - `{target}`\n    `{html}`")
    if len(nodes) > 5:
        lines.append(f"  - ... and {len(nodes) - 5} more")
    return "\n".join(lines)


async def scan_page(page: Page, url: str) -> dict | None:
    """Scan a single page with axe-core. Returns results or None on failure."""
    await page.goto(url, wait_until="domcontentloaded")
    await asyncio.sleep(2)  # Let dynamic content settle

    if not await _inject_axe(page):
        return None

    return await _run_axe(page)


def _page_label(page_url: str, base_url: str) -> str:
    """Short label for a page URL — shows the full URL for clarity."""
    return page_url


def generate_wcag_markdown(results: list[dict], url: str) -> str:
    """Generate a markdown WCAG scan report with per-page breakdown."""
    lines = [
        "# WCAG 2.2 AA Accessibility Scan Report\n",
        f"**URL:** {url}",
        f"**Date:** {date.today().isoformat()}",
        f"**Engine:** axe-core 4.10.2",
        f"**Standard:** WCAG 2.2 Level AA",
        f"**Pages scanned:** {len(results)}",
        "",
    ]

    # Aggregate totals for the summary
    all_violation_ids = set()
    all_pass_ids = set()
    all_incomplete_ids = set()
    total_issues = 0
    for r in results:
        for v in r.get("violations", []):
            all_violation_ids.add(v["id"])
            total_issues += len(v.get("nodes", []))
        all_pass_ids.update(p["id"] for p in r.get("passes", []))
        all_incomplete_ids.update(i["id"] for i in r.get("incomplete", []))

    total_violations = len(all_violation_ids)

    # Score
    if total_violations == 0:
        score = "PASS — No violations found"
        score_note = "All automated WCAG 2.2 AA checks passed across all pages."
    else:
        critical = 0
        serious = 0
        for r in results:
            for v in r.get("violations", []):
                if v.get("impact") == "critical":
                    critical += 1
                elif v.get("impact") == "serious":
                    serious += 1
        if critical > 0:
            score = f"FAIL — {total_violations} rules violated ({total_issues} issues)"
        elif serious > 0:
            score = f"NEEDS WORK — {total_violations} rules violated ({total_issues} issues)"
        else:
            score = f"MINOR ISSUES — {total_violations} rules violated ({total_issues} issues)"
        score_note = f"{critical} critical, {serious} serious across {len(results)} page(s)."

    lines.append(f"## Result: {score}\n")
    lines.append(f"{score_note}\n")

    # Summary table
    lines.append("## Summary\n")
    lines.append("| Category | Count |")
    lines.append("|----------|-------|")
    lines.append(f"| Pages scanned | {len(results)} |")
    lines.append(f"| Rules violated | {total_violations} |")
    lines.append(f"| Total issues (elements) | {total_issues} |")
    lines.append(f"| Rules passed | {len(all_pass_ids)} |")
    lines.append(f"| Needs manual review | {len(all_incomplete_ids)} |")
    lines.append("")

    # Pages scanned
    lines.append("## Pages Scanned\n")
    lines.append("| # | Page | Violations | Passed | Needs Review |")
    lines.append("|---|------|-----------|--------|--------------|")
    for i, r in enumerate(results, 1):
        page_url = r.get("url", "unknown")
        label = _page_label(page_url, url)
        v_count = len(r.get("violations", []))
        p_count = len(r.get("passes", []))
        inc_count = len(r.get("incomplete", []))
        v_status = f"**{v_count}**" if v_count > 0 else "0"
        lines.append(f"| {i} | {label} | {v_status} | {p_count} | {inc_count} |")
    lines.append("")

    # Per-page detailed breakdown
    for i, r in enumerate(results, 1):
        page_url = r.get("url", "unknown")
        label = _page_label(page_url, url)
        violations = r.get("violations", [])
        passes = r.get("passes", [])
        incomplete = r.get("incomplete", [])

        lines.append(f"---\n")
        lines.append(f"## Page {i}: {label}\n")
        lines.append(f"**URL:** {page_url}\n")

        # Violations for this page
        if violations:
            lines.append(f"### Violations ({len(violations)} rules)\n")
            lines.append("| Impact | Rule | Description | Elements |")
            lines.append("|--------|------|-------------|----------|")
            sorted_v = sorted(violations, key=lambda v: IMPACT_ORDER.get(v.get("impact", "minor"), 4))
            for v in sorted_v:
                impact = v.get("impact", "unknown").upper()
                nodes = v.get("nodes", [])
                lines.append(f"| {impact} | {v['id']} | {v.get('help', '')} | {len(nodes)} |")
            lines.append("")

            # Detail per violation
            for v in sorted_v:
                nodes = v.get("nodes", [])
                tags = ", ".join(t for t in v.get("tags", []) if t.startswith("wcag"))
                ref = f" — [reference]({v['helpUrl']})" if v.get("helpUrl") else ""
                lines.append(f"**{v['id']}** ({tags}){ref}\n")
                lines.append(f"{_format_nodes(nodes)}\n")
        else:
            lines.append("### Violations\n")
            lines.append("None\n")

        # Passed for this page
        lines.append(f"### Passed ({len(passes)} rules)\n")
        if passes:
            lines.append("| Rule | Description |")
            lines.append("|------|-------------|")
            for p in sorted(passes, key=lambda x: x["id"]):
                lines.append(f"| {p['id']} | {p.get('help', p.get('description', ''))} |")
            lines.append("")
        else:
            lines.append("None\n")

        # Incomplete for this page
        if incomplete:
            lines.append(f"### Needs Manual Review ({len(incomplete)} rules)\n")
            for inc in sorted(incomplete, key=lambda x: x["id"]):
                nodes = inc.get("nodes", [])
                tags = ", ".join(t for t in inc.get("tags", []) if t.startswith("wcag"))
                ref = f" — [reference]({inc['helpUrl']})" if inc.get("helpUrl") else ""
                lines.append(f"**{inc['id']}** ({tags}){ref}: {inc.get('help', inc.get('description', ''))}\n")
                if nodes:
                    lines.append(f"Elements to review ({len(nodes)}):\n")
                    lines.append(f"{_format_nodes(nodes)}\n")
                else:
                    lines.append("No specific elements — manual page review needed.\n")

    return "\n".join(lines)



def _build_html_elements(nodes: list, color: str = "#64748b") -> str:
    """Build HTML showing affected elements with selectors and HTML snippets."""
    if not nodes:
        return ""
    items = ""
    for node in nodes[:5]:
        target = _esc(", ".join(node.get("target", [])))
        html_snippet = _esc(node.get("html", "")[:150])
        failure = _esc(node.get("failureSummary", ""))
        items += f"""<div style="background:#f8fafc;border-left:3px solid {color};padding:8px 12px;margin:4px 0;border-radius:0 6px 6px 0">
            <code style="font-size:12px;color:#1e293b;display:block">{target}</code>
            <code style="font-size:11px;color:#64748b;display:block;margin-top:2px">{html_snippet}</code>
            {f'<div style="font-size:11px;color:{color};margin-top:4px">{failure}</div>' if failure else ''}
        </div>"""
    if len(nodes) > 5:
        items += f'<p style="font-size:11px;color:#94a3b8;margin-top:4px">... and {len(nodes)-5} more elements</p>'
    return items


def _build_html_page_section(page_result: dict, page_num: int, base_url: str) -> str:
    """Build HTML for a single page's results."""
    page_url = page_result.get("url", "unknown")
    label = _page_label(page_url, base_url)
    violations = page_result.get("violations", [])
    passes = page_result.get("passes", [])
    incomplete = page_result.get("incomplete", [])
    impact_colors = {"critical": "#dc2626", "serious": "#ea580c", "moderate": "#d97706", "minor": "#6b7280"}

    # Violations — summary table + detail blocks
    violations_html = ""
    if violations:
        sorted_v = sorted(violations, key=lambda v: IMPACT_ORDER.get(v.get("impact", "minor"), 4))

        # Summary table
        v_rows = ""
        for v in sorted_v:
            impact = v.get("impact", "unknown")
            ic = impact_colors.get(impact, "#6b7280")
            nodes = v.get("nodes", [])
            help_url = v.get("helpUrl", "")
            link = f' <a href="{help_url}" style="font-size:11px">[more]</a>' if help_url else ""
            v_rows += f"""<tr>
                <td><span style="background:{ic}22;color:{ic};padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600">{impact.upper()}</span></td>
                <td><strong>{_esc(v['id'])}</strong>{link}</td>
                <td>{_esc(v.get('help', ''))}</td>
                <td>{len(nodes)}</td>
            </tr>"""

        # Detail blocks per violation
        detail_blocks = ""
        for v in sorted_v:
            impact = v.get("impact", "unknown")
            ic = impact_colors.get(impact, "#6b7280")
            nodes = v.get("nodes", [])
            tags = ", ".join(t for t in v.get("tags", []) if t.startswith("wcag"))
            help_url = v.get("helpUrl", "")
            link = f'<a href="{help_url}">Learn more</a>' if help_url else ""
            detail_blocks += f"""
            <div style="margin:1rem 0;padding:12px;background:#fef2f2;border-radius:8px;border:1px solid #fecaca">
                <div style="font-weight:600;color:{ic};margin-bottom:4px">{_esc(v['id'])} — {_esc(v.get('help', ''))} [{impact.upper()}]</div>
                <div style="font-size:12px;color:#64748b;margin-bottom:8px">WCAG: {tags} {link}</div>
                <div style="font-size:12px;font-weight:600;margin-bottom:4px">Affected elements ({len(nodes)}):</div>
                {_build_html_elements(nodes, ic)}
            </div>"""

        violations_html = f"""<h3 style="color:#dc2626;margin:1rem 0 0.5rem">Violations ({len(violations)})</h3>
            <table><thead><tr><th>Impact</th><th>Rule</th><th>Description</th><th>Elements</th></tr></thead>
            <tbody>{v_rows}</tbody></table>
            {detail_blocks}"""
    else:
        violations_html = '<p style="color:#16a34a;font-weight:600;margin:0.5rem 0">No violations</p>'

    # Passed table
    p_rows = ""
    for p in sorted(passes, key=lambda x: x["id"]):
        p_rows += f'<tr><td style="color:#16a34a;font-weight:600">PASS</td><td>{_esc(p["id"])}</td><td>{_esc(p.get("help", p.get("description", "")))}</td></tr>'
    passed_html = f"""<h3 style="color:#16a34a;margin:1rem 0 0.5rem">Passed ({len(passes)})</h3>
        <table><thead><tr><th>Status</th><th>Rule</th><th>Description</th></tr></thead>
        <tbody>{p_rows}</tbody></table>""" if p_rows else ""

    # Incomplete — with affected elements
    incomplete_html = ""
    if incomplete:
        inc_blocks = ""
        for inc in sorted(incomplete, key=lambda x: x["id"]):
            nodes = inc.get("nodes", [])
            tags = ", ".join(t for t in inc.get("tags", []) if t.startswith("wcag"))
            help_url = inc.get("helpUrl", "")
            link = f'<a href="{help_url}">Learn more</a>' if help_url else ""
            elements = _build_html_elements(nodes, "#d97706") if nodes else '<div style="font-size:12px;color:#94a3b8">No specific elements identified — manual page review needed</div>'
            inc_blocks += f"""
            <div style="margin:1rem 0;padding:12px;background:#fffbeb;border-radius:8px;border:1px solid #fde68a">
                <div style="font-weight:600;color:#d97706;margin-bottom:4px">{_esc(inc['id'])} — {_esc(inc.get('help', inc.get('description', '')))}</div>
                <div style="font-size:12px;color:#64748b;margin-bottom:8px">WCAG: {tags} {link}</div>
                <div style="font-size:12px;font-weight:600;margin-bottom:4px">Elements to review ({len(nodes)}):</div>
                {elements}
            </div>"""

        incomplete_html = f"""<h3 style="color:#d97706;margin:1rem 0 0.5rem">Needs Manual Review ({len(incomplete)})</h3>
            {inc_blocks}"""

    v_badge = f'<span style="color:#dc2626;font-weight:600">{len(violations)} violations</span>' if violations else '<span style="color:#16a34a;font-weight:600">0 violations</span>'

    return f"""
    <div class="section">
        <h2>Page {page_num}: {label} — {v_badge}, {len(passes)} passed, {len(incomplete)} review</h2>
        <p style="font-size:0.8rem;color:#64748b;margin-bottom:1rem">{page_url}</p>
        {violations_html}
        {passed_html}
        {incomplete_html}
    </div>"""


def generate_wcag_html(results: list[dict], url: str) -> str:
    """Generate a standalone HTML WCAG scan report with per-page breakdown."""
    # Aggregate totals
    all_violation_ids = set()
    total_issues = 0
    all_pass_ids = set()
    all_incomplete_ids = set()
    for r in results:
        for v in r.get("violations", []):
            all_violation_ids.add(v["id"])
            total_issues += len(v.get("nodes", []))
        all_pass_ids.update(p["id"] for p in r.get("passes", []))
        all_incomplete_ids.update(i["id"] for i in r.get("incomplete", []))

    total_violations = len(all_violation_ids)

    if total_violations == 0:
        score_label = "PASS"
        score_color = "#16a34a"
        score_detail = "No WCAG 2.2 AA violations found"
    else:
        critical = sum(1 for r in results for v in r.get("violations", []) if v.get("impact") == "critical")
        serious = sum(1 for r in results for v in r.get("violations", []) if v.get("impact") == "serious")
        if critical > 0:
            score_label = "FAIL"
            score_color = "#dc2626"
        elif serious > 0:
            score_label = "NEEDS WORK"
            score_color = "#d97706"
        else:
            score_label = "MINOR ISSUES"
            score_color = "#d97706"
        score_detail = f"{total_violations} rules violated, {total_issues} elements affected across {len(results)} page(s)"

    # Build per-page overview table
    overview_rows = ""
    for i, r in enumerate(results, 1):
        page_url = r.get("url", "unknown")
        label = _page_label(page_url, url)
        v_count = len(r.get("violations", []))
        p_count = len(r.get("passes", []))
        inc_count = len(r.get("incomplete", []))
        v_style = 'color:#dc2626;font-weight:600' if v_count > 0 else 'color:#16a34a'
        overview_rows += f'<tr><td>{i}</td><td>{label}</td><td style="{v_style}">{v_count}</td><td style="color:#16a34a">{p_count}</td><td style="color:#d97706">{inc_count}</td></tr>'

    # Build per-page sections
    page_sections = ""
    for i, r in enumerate(results, 1):
        page_sections += _build_html_page_section(r, i, url)

    today = date.today().isoformat()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WCAG 2.2 AA Scan — {url}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #1e293b; line-height: 1.6; padding: 2rem; }}
    .container {{ max-width: 1100px; margin: 0 auto; }}
    .header {{ background: #1e293b; color: #fff; padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; }}
    .header h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
    .meta {{ display: flex; gap: 2rem; font-size: 0.875rem; color: #94a3b8; margin-top: 0.5rem; flex-wrap: wrap; }}
    .score {{ background: {score_color}11; border: 2px solid {score_color}; border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1.5rem; }}
    .score h2 {{ color: {score_color}; font-size: 1.75rem; }}
    .score .detail {{ color: #64748b; margin-top: 0.25rem; }}
    .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }}
    .stat {{ background: #fff; border-radius: 12px; padding: 1.25rem; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
    .stat .number {{ font-size: 2rem; font-weight: 700; }}
    .stat .label {{ font-size: 0.8rem; color: #64748b; }}
    .section {{ background: #fff; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
    .section h2 {{ font-size: 1.125rem; margin-bottom: 1rem; color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
    .section h3 {{ font-size: 1rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
    th {{ background: #f1f5f9; padding: 0.6rem; text-align: left; font-weight: 600; color: #475569; }}
    td {{ padding: 0.6rem; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    tr:hover {{ background: #f8fafc; }}
    code {{ background: #f1f5f9; padding: 1px 4px; border-radius: 3px; font-size: 12px; }}
    a {{ color: #2563eb; }}
    .footer {{ text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 2rem; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>WCAG 2.2 AA Accessibility Scan</h1>
        <div class="meta">
            <span>URL: {url}</span>
            <span>Date: {today}</span>
            <span>Engine: axe-core 4.10.2</span>
            <span>Pages: {len(results)}</span>
        </div>
    </div>

    <div class="score">
        <h2>{score_label}</h2>
        <div class="detail">{score_detail}</div>
    </div>

    <div class="stats">
        <div class="stat"><div class="number" style="color:#dc2626">{total_violations}</div><div class="label">Rules Violated</div></div>
        <div class="stat"><div class="number" style="color:#ea580c">{total_issues}</div><div class="label">Elements Affected</div></div>
        <div class="stat"><div class="number" style="color:#16a34a">{len(all_pass_ids)}</div><div class="label">Rules Passed</div></div>
        <div class="stat"><div class="number" style="color:#6b7280">{len(all_incomplete_ids)}</div><div class="label">Needs Review</div></div>
    </div>

    <div class="section">
        <h2>Pages Overview</h2>
        <table>
            <thead><tr><th>#</th><th>Page</th><th>Violations</th><th>Passed</th><th>Needs Manual Review</th></tr></thead>
            <tbody>{overview_rows}</tbody>
        </table>
    </div>

    {page_sections}

    <div class="footer">
        Generated by Cookie Consent Compliance QA Agent — WCAG Scanner | axe-core 4.10.2
    </div>
</div>
</body>
</html>"""


async def run_wcag_scan(
    url: str,
    pages: list[str] | None = None,
    headless: bool = True,
    output_dir: str | None = None,
) -> None:
    """Run a full WCAG 2.2 AA scan on one or more pages."""

    site_dir = Path(output_dir) if output_dir else get_output_dir(url)
    site_dir.mkdir(parents=True, exist_ok=True)

    # Build page list
    urls_to_scan = [url]
    if pages:
        urls_to_scan.extend(urljoin(url, p) for p in pages)

    all_results = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Launching browser...", total=None)

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            page = await context.new_page()

            for i, scan_url in enumerate(urls_to_scan, 1):
                progress.update(task, description=f"Scanning page {i}/{len(urls_to_scan)}: {scan_url}")
                result = await scan_page(page, scan_url)
                if result:
                    all_results.append(result)

                    # Print per-page summary
                    label = _page_label(scan_url, url)
                    v_count = len(result.get("violations", []))
                    p_count = len(result.get("passes", []))
                    inc_count = len(result.get("incomplete", []))
                    if v_count == 0:
                        console.print(f"  [green]{label}: {p_count} passed, 0 violations, {inc_count} need review[/green]")
                    else:
                        console.print(f"  [yellow]{label}: {p_count} passed, {v_count} violations, {inc_count} need review[/yellow]")
                else:
                    console.print(f"  [red]Page {i}: scan failed[/red]")

            # Take a screenshot
            progress.update(task, description="Capturing screenshot...")
            screenshot_path = site_dir / "wcag-screenshot.png"
            await page.screenshot(path=str(screenshot_path))

            await browser.close()

        progress.update(task, description="Generating reports...")

    if not all_results:
        console.print("[red]No pages could be scanned.[/red]")
        return

    # Save raw results
    raw_path = site_dir / "wcag-raw-results.json"
    raw_path.write_text(json.dumps(all_results, indent=2))

    # Generate reports
    md = generate_wcag_markdown(all_results, url)
    md_path = site_dir / "wcag-report.md"
    md_path.write_text(md)

    html = generate_wcag_html(all_results, url)
    html_path = site_dir / "wcag-report.html"
    html_path.write_text(html)

    # Print summary
    all_violations = []
    for r in all_results:
        all_violations.extend(r.get("violations", []))

    violation_ids = set(v["id"] for v in all_violations)
    total_issues = sum(len(v.get("nodes", [])) for v in all_violations)

    console.print()
    if not violation_ids:
        console.print(Panel(
            "[bold green]PASS — No WCAG 2.2 AA violations found[/bold green]",
            border_style="green",
        ))
    else:
        # Count by impact
        impact_counts = {}
        for v in all_violations:
            imp = v.get("impact", "unknown")
            if v["id"] not in impact_counts:
                impact_counts[imp] = impact_counts.get(imp, 0) + 1

        table = Table(title="WCAG 2.2 AA Violations", show_header=True, header_style="bold")
        table.add_column("Impact")
        table.add_column("Rule")
        table.add_column("Description")
        table.add_column("Elements", justify="right")

        seen = set()
        sorted_v = sorted(all_violations, key=lambda v: IMPACT_ORDER.get(v.get("impact", "minor"), 4))
        for v in sorted_v:
            if v["id"] in seen:
                continue
            seen.add(v["id"])
            impact = v.get("impact", "unknown")
            table.add_row(
                f"[{_impact_style(impact)}]{impact.upper()}[/{_impact_style(impact)}]",
                v["id"],
                v.get("help", v.get("description", "")),
                str(len(v.get("nodes", []))),
            )

        console.print(table)

    # Print passed rules
    all_passes = []
    all_incomplete = []
    for r in all_results:
        all_passes.extend(r.get("passes", []))
        all_incomplete.extend(r.get("incomplete", []))

    pass_ids = set()
    pass_table = Table(title=f"Passed Rules ({len(set(p['id'] for p in all_passes))})", show_header=True, header_style="bold green")
    pass_table.add_column("Rule", style="green")
    pass_table.add_column("Description")
    for p in sorted(all_passes, key=lambda x: x["id"]):
        if p["id"] not in pass_ids:
            pass_ids.add(p["id"])
            pass_table.add_row(p["id"], p.get("help", p.get("description", "")))

    if pass_ids:
        console.print()
        console.print(pass_table)

    # Print incomplete (needs manual review)
    inc_ids = set()
    if all_incomplete:
        console.print()
        inc_table = Table(title=f"Needs Manual Review ({len(set(i['id'] for i in all_incomplete))})", show_header=True, header_style="bold yellow")
        inc_table.add_column("Rule", style="yellow")
        inc_table.add_column("Description")
        for inc in sorted(all_incomplete, key=lambda x: x["id"]):
            if inc["id"] not in inc_ids:
                inc_ids.add(inc["id"])
                inc_table.add_row(inc["id"], inc.get("help", inc.get("description", "")))
        console.print(inc_table)

    console.print(f"\n[green]Markdown report: {md_path}[/green]")
    console.print(f"[green]HTML report: {html_path}[/green]")
    console.print(f"[dim]Raw results: {raw_path}[/dim]")
