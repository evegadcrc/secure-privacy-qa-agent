"""Generate an Excel workbook of manual compliance test cases.

Scans the target site with Playwright to gather context (banner, cookies,
buttons), then generates test cases tailored to what was found — organized
by compliance framework with one sheet per framework.

Usage:
    python -m src.main generate-tests https://example.com
    python -m src.main generate-tests https://example.com --frameworks GDPR,CNIL
    python -m src.main generate-tests https://example.com --output my-tests.xlsx
"""

import asyncio
from datetime import date, datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from playwright.async_api import async_playwright
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..banner_detector import detect_banner
from ..cookie_inspector import capture_cookies
from .compliance_frameworks import (
    ComplianceCheck,
    ALL_CHECKS,
    ALL_FRAMEWORKS,
    get_checks_by_framework,
)

console = Console()

# --- Styles ---
HEADER_FONT = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
HEADER_FILL = PatternFill(start_color="2F5496", end_color="2F5496", fill_type="solid")
HEADER_ALIGNMENT = Alignment(horizontal="center", vertical="center", wrap_text=True)

SEVERITY_FILLS = {
    "critical": PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"),
    "major": PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"),
    "minor": PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"),
}
SEVERITY_FONTS = {
    "critical": Font(color="9C0006"),
    "major": Font(color="9C6500"),
    "minor": Font(color="006100"),
}

PASS_FILL = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
FAIL_FILL = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
WARN_FILL = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")

THIN_BORDER = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)

WRAP_ALIGNMENT = Alignment(vertical="top", wrap_text=True)

COLUMNS = [
    ("ID", 12),
    ("Category", 18),
    ("Check", 35),
    ("Severity", 12),
    ("Description", 50),
    ("Precondition", 35),
    ("Test Steps", 60),
    ("Expected Result", 45),
    ("Automated?", 12),
    ("Site Context", 45),
    ("Actual Result", 35),
    ("Status", 12),
    ("Tester", 15),
    ("Date", 12),
    ("Notes", 40),
]


def _build_precondition(check: ComplianceCheck) -> str:
    """Derive a precondition from the check steps."""
    steps_text = " ".join(check.steps).lower()
    conditions = []
    if "fresh" in steps_text or "clear" in steps_text:
        conditions.append("Fresh browser session (clear all cookies and storage)")
    if "preference center" in steps_text or "settings" in steps_text:
        conditions.append("Consent banner must be visible with preference center accessible")
    if "accept" in steps_text and "after" in steps_text:
        conditions.append("Consent has been given (Accept All clicked)")
    if not conditions:
        conditions.append("Navigate to the target URL")
    return "\n".join(conditions)


def _build_site_context(check: ComplianceCheck, site_context: dict) -> str:
    """Build a contextual note based on the site scan."""
    lines = []

    if check.automated:
        # Add automated scan findings
        tracking = site_context.get("tracking_before_consent", [])
        if "pre-consent" in check.title.lower() or "prior consent" in check.title.lower() or check.id in ("GDPR-001", "EPRIV-001", "ICO-001"):
            if tracking:
                lines.append(f"SCAN: {len(tracking)} tracking cookie(s) BEFORE consent: {', '.join(tracking)}")
            else:
                lines.append("SCAN: No tracking cookies detected before consent.")

        if "reject" in check.title.lower() and site_context.get("buttons"):
            reject_kw = ["reject", "decline", "deny", "refuse"]
            has_reject = any(any(kw in b.lower() for kw in reject_kw) for b in site_context["buttons"])
            if has_reject:
                lines.append(f"SCAN: Reject button found: {', '.join(site_context['buttons'])}")
            else:
                lines.append(f"SCAN: No reject button detected. Buttons: {', '.join(site_context['buttons']) or 'N/A'}")

    if "third-party" in check.title.lower() or "third party" in check.title.lower():
        tp = site_context.get("third_party_domains", [])
        if tp:
            lines.append(f"SCAN: Third-party cookie domains: {', '.join(tp)}")

    if not lines:
        banner_status = "detected" if site_context.get("banner_found") else "NOT detected"
        lines.append(f"Banner: {banner_status}")
        if site_context.get("buttons"):
            lines.append(f"Buttons: {', '.join(site_context['buttons'])}")
        lines.append(f"Pre-consent cookies: {site_context.get('total_cookies_before', 0)}")

    return "\n".join(lines)


def _add_framework_sheet(wb: Workbook, framework: str, checks: list[ComplianceCheck], site_context: dict) -> None:
    """Add a worksheet for a single framework."""
    # Sanitize sheet name (max 31 chars)
    sheet_name = framework[:31]
    ws = wb.create_sheet(title=sheet_name)

    # Write headers
    for col_idx, (col_name, col_width) in enumerate(COLUMNS, 1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGNMENT
        cell.border = THIN_BORDER
        ws.column_dimensions[get_column_letter(col_idx)].width = col_width

    # Freeze top row
    ws.freeze_panes = "A2"

    # Add auto-filter
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}1"

    # Write checks
    for row_idx, check in enumerate(checks, 2):
        steps_text = "\n".join(f"{i}. {s}" for i, s in enumerate(check.steps, 1))
        precondition = _build_precondition(check)
        context = _build_site_context(check, site_context)

        row_data = [
            check.id,
            check.category,
            check.title,
            check.severity.upper(),
            check.description,
            precondition,
            steps_text,
            check.expected,
            "Yes" if check.automated else "No",
            context,
            "",  # Actual Result — blank for tester
            "",  # Status — blank for tester
            "",  # Tester — blank
            "",  # Date — blank
            "",  # Notes — blank
        ]

        for col_idx, value in enumerate(row_data, 1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = WRAP_ALIGNMENT
            cell.border = THIN_BORDER

        # Style severity column
        severity_cell = ws.cell(row=row_idx, column=4)
        if check.severity in SEVERITY_FILLS:
            severity_cell.fill = SEVERITY_FILLS[check.severity]
            severity_cell.font = SEVERITY_FONTS[check.severity]

        # Add data validation for Status column
        from openpyxl.worksheet.datavalidation import DataValidation
        status_cell = ws.cell(row=row_idx, column=12)
        dv = DataValidation(type="list", formula1='"PASS,FAIL,WARNING,SKIP,N/A"', allow_blank=True)
        dv.error = "Please select: PASS, FAIL, WARNING, SKIP, or N/A"
        dv.errorTitle = "Invalid Status"
        ws.add_data_validation(dv)
        dv.add(status_cell)

    # Set row height for better readability
    for row_idx in range(2, len(checks) + 2):
        ws.row_dimensions[row_idx].height = 80


def _add_summary_sheet(wb: Workbook, checks: list[ComplianceCheck], site_context: dict, url: str) -> None:
    """Add a summary/overview sheet as the first sheet."""
    ws = wb.create_sheet(title="Overview", index=0)

    # Title
    ws.merge_cells("A1:F1")
    title_cell = ws.cell(row=1, column=1, value="Cookie Consent Compliance — Manual Test Plan")
    title_cell.font = Font(name="Calibri", bold=True, size=16, color="2F5496")
    title_cell.alignment = Alignment(horizontal="center")

    # Metadata
    meta = [
        ("Target URL:", url),
        ("Generated:", datetime.now().strftime("%Y-%m-%d %H:%M")),
        ("Total Checks:", str(len(checks))),
        ("Frameworks:", ", ".join(sorted(set(c.framework for c in checks)))),
        ("Banner Detected:", "Yes" if site_context.get("banner_found") else "No"),
        ("Buttons Found:", ", ".join(site_context.get("buttons", [])) or "None (iframe)"),
        ("Pre-consent Cookies:", str(site_context.get("total_cookies_before", 0))),
        ("Tracking Before Consent:", ", ".join(site_context.get("tracking_before_consent", [])) or "None"),
    ]

    for i, (label, value) in enumerate(meta, 3):
        ws.cell(row=i, column=1, value=label).font = Font(bold=True)
        ws.cell(row=i, column=2, value=value)

    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 60

    # Framework summary table
    row = len(meta) + 5
    ws.cell(row=row, column=1, value="Framework Summary").font = Font(bold=True, size=13)
    row += 1

    headers = ["Framework", "Total Checks", "Critical", "Major", "Minor", "Automated"]
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=row, column=col, value=header)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.border = THIN_BORDER

    for fw_name in sorted(set(c.framework for c in checks)):
        row += 1
        fw_checks = [c for c in checks if c.framework == fw_name]
        ws.cell(row=row, column=1, value=fw_name).border = THIN_BORDER
        ws.cell(row=row, column=2, value=len(fw_checks)).border = THIN_BORDER
        ws.cell(row=row, column=3, value=sum(1 for c in fw_checks if c.severity == "critical")).border = THIN_BORDER
        ws.cell(row=row, column=4, value=sum(1 for c in fw_checks if c.severity == "major")).border = THIN_BORDER
        ws.cell(row=row, column=5, value=sum(1 for c in fw_checks if c.severity == "minor")).border = THIN_BORDER
        ws.cell(row=row, column=6, value=sum(1 for c in fw_checks if c.automated)).border = THIN_BORDER

    # Instructions
    row += 3
    ws.cell(row=row, column=1, value="Instructions").font = Font(bold=True, size=13)
    row += 1
    instructions = [
        "1. Each framework has its own sheet with detailed test cases.",
        "2. For each check: follow the Test Steps, compare with Expected Result.",
        "3. Record your findings in the 'Actual Result' column.",
        "4. Set the Status column to PASS, FAIL, WARNING, SKIP, or N/A.",
        "5. Add your name in the Tester column and the date you performed the test.",
        "6. Use the Notes column for any additional observations.",
        "7. Checks marked 'Automated: Yes' have pre-scan context in the 'Site Context' column.",
        "8. Priority: address CRITICAL severity findings first, then MAJOR, then MINOR.",
    ]
    for instruction in instructions:
        ws.cell(row=row, column=1, value=instruction)
        row += 1


async def scan_site_context(url: str) -> dict:
    """Scan the site to gather context for generating tailored test cases."""
    context_data = {
        "url": url,
        "banner_found": False,
        "banner_text": "",
        "buttons": [],
        "total_cookies_before": 0,
        "tracking_before_consent": [],
        "all_cookies_before": [],
        "third_party_domains": [],
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = await ctx.new_page()

        await page.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Capture pre-consent cookies
        cookies = await capture_cookies(ctx)
        context_data["total_cookies_before"] = len(cookies)
        context_data["all_cookies_before"] = [c.model_dump() for c in cookies]
        context_data["tracking_before_consent"] = [
            c.name for c in cookies if c.category in ("analytics", "marketing")
        ]

        # Identify third-party domains
        page_domain = url.split("//")[-1].split("/")[0]
        base_domain = ".".join(page_domain.split(".")[-2:])
        third_party = set()
        for c in cookies:
            cookie_base = ".".join(c.domain.lstrip(".").split(".")[-2:])
            if cookie_base != base_domain:
                third_party.add(c.domain)
        context_data["third_party_domains"] = sorted(third_party)

        # Detect banner
        banner = await detect_banner(page, url)
        context_data["banner_found"] = banner.banner_found
        context_data["banner_text"] = banner.text or ""
        context_data["buttons"] = banner.buttons

        await browser.close()

    return context_data


async def generate_test_cases(
    url: str,
    frameworks: list[str] | None = None,
    output: str | None = None,
) -> str:
    """Scan the site and generate an Excel workbook of manual test cases.

    Returns the path to the generated Excel file.
    """
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
        console.print("[red]No checks selected.[/red]")
        return ""

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Scanning site for context...", total=None)

        # Scan site
        site_context = await scan_site_context(url)
        progress.update(task, description=f"Banner: {'found' if site_context['banner_found'] else 'not found'}, {site_context['total_cookies_before']} pre-consent cookies")

        # Generate workbook
        progress.update(task, description="Generating Excel test cases...")

        wb = Workbook()
        # Remove default sheet
        wb.remove(wb.active)

        # Add summary sheet
        _add_summary_sheet(wb, checks, site_context, url)

        # Add per-framework sheets
        seen_frameworks = []
        for check in checks:
            if check.framework not in seen_frameworks:
                seen_frameworks.append(check.framework)

        for fw in seen_frameworks:
            fw_checks = [c for c in checks if c.framework == fw]
            _add_framework_sheet(wb, fw, fw_checks, site_context)

        # Determine output path
        if output is None:
            domain = url.split("//")[-1].split("/")[0].replace(".", "-")
            output = f"compliance-tests-{domain}.xlsx"

        Path(output).parent.mkdir(parents=True, exist_ok=True)
        wb.save(output)
        progress.update(task, description="Done!")

    # Print summary
    console.print(f"\n[green]Test cases generated: {output}[/green]")
    console.print(f"  Checks: {len(checks)} across {len(seen_frameworks)} framework(s)")
    console.print(f"  Sheets: Overview + {', '.join(seen_frameworks)}")

    if site_context["tracking_before_consent"]:
        console.print(
            f"  [red]Pre-scan alert: {len(site_context['tracking_before_consent'])} tracking cookie(s) "
            f"found before consent: {', '.join(site_context['tracking_before_consent'])}[/red]"
        )

    return output
