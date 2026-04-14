from datetime import date
from pathlib import Path

from .models import ComplianceReport, Status, CookieInfo
from .cookie_inspector import is_tracking_cookie

VERSION = "1.0.0"


def _status_icon(status: Status) -> str:
    if status == Status.PASS:
        return "PASS"
    elif status == Status.FAIL:
        return "FAIL"
    else:
        return "WARN"


def _severity_label(severity) -> str:
    if severity is None:
        return "-"
    return severity.value.capitalize()


def _count_tracking(cookies: list[CookieInfo]) -> int:
    return sum(1 for c in cookies if is_tracking_cookie(c))


def _cookie_phase_status(cookies: list[CookieInfo], phase: str) -> str:
    tracking = _count_tracking(cookies)
    if phase == "before":
        return "PASS" if tracking == 0 else "FAIL"
    elif phase == "accept":
        return "Expected"
    elif phase == "reject":
        return "PASS" if tracking == 0 else "FAIL"
    return "-"


def generate_report(report: ComplianceReport) -> str:
    """Generate a markdown compliance report."""
    lines = []

    # Header
    lines.append("# Cookie Consent Compliance Report\n")
    lines.append(f"**URL:** {report.url}")
    lines.append(f"**Date:** {date.today().isoformat()}")
    lines.append(f"**Agent Version:** {VERSION}")
    lines.append("")

    # Overall score
    passed = sum(1 for f in report.findings if f.status == Status.PASS)
    total = len(report.findings)
    score_label = report.overall_score.upper()
    if report.overall_score == "partial":
        score_label = "PARTIAL COMPLIANCE"
    elif report.overall_score == "pass":
        score_label = "COMPLIANT"
    elif report.overall_score == "fail":
        score_label = "NON-COMPLIANT"
    elif report.overall_score == "pending":
        score_label = "PENDING AI ANALYSIS"
    elif report.overall_score == "not_applicable":
        score_label = "NOT APPLICABLE — NO BANNER DETECTED"

    lines.append(f"## Overall Score: {score_label} ({passed}/{total} checks passed)\n")

    # Summary
    lines.append(f"## Summary\n")
    lines.append(f"{report.summary}\n")

    # Findings table
    lines.append("## Findings\n")
    lines.append("| # | Framework | Rule | Check | Status | Severity | Detail |")
    lines.append("|---|-----------|------|-------|--------|----------|--------|")
    for i, f in enumerate(report.findings, 1):
        fw = f.framework or "-"
        rule = f.rule_id or "-"
        lines.append(
            f"| {i} | {fw} | {rule} | {f.criterion} | {_status_icon(f.status)} | "
            f"{_severity_label(f.severity)} | {f.detail} |"
        )
    lines.append("")

    # Cookie behavior table
    lines.append("## Cookie Behavior\n")
    lines.append("| Phase | Cookies Found | Tracking Cookies | Status |")
    lines.append("|-------|--------------|-----------------|--------|")

    audit = report.cookie_audit
    for phase, cookies in [
        ("Before consent", audit.cookies_before_consent),
        ("After accept", audit.cookies_after_accept),
        ("After reject", audit.cookies_after_reject),
    ]:
        phase_key = phase.split()[-1].lower()
        if phase_key == "consent":
            phase_key = "before"
        lines.append(
            f"| {phase} | {len(cookies)} | {_count_tracking(cookies)} | "
            f"{_cookie_phase_status(cookies, phase_key)} |"
        )
    lines.append("")

    # Cookie violations
    if audit.violations:
        lines.append("### Cookie Violations\n")
        for v in audit.violations:
            lines.append(f"- {v}")
        lines.append("")

    # Flow test results
    if report.flow_results:
        lines.append("## Consent Flow Tests\n")
        lines.append("| Action | Banner Dismissed | Tracking Cookies Set | Result |")
        lines.append("|--------|-----------------|---------------------|--------|")
        for fr in report.flow_results:
            lines.append(
                f"| {fr.action.capitalize()} | "
                f"{'Yes' if fr.banner_dismissed else 'No'} | "
                f"{'Yes' if fr.tracking_cookies_set else 'No'} | "
                f"{'PASS' if fr.passed else 'FAIL'} |"
            )
        lines.append("")

    # Recommendations
    if report.recommendations:
        lines.append("## Recommendations\n")
        for i, rec in enumerate(report.recommendations, 1):
            lines.append(f"{i}. {rec}")
        lines.append("")

    # Evidence
    evidence_paths = []
    if report.flow_results:
        for fr in report.flow_results:
            if fr.screenshot_path:
                evidence_paths.append(
                    f"- [{fr.action.capitalize()} flow screenshot]({fr.screenshot_path})"
                )

    if evidence_paths:
        lines.append("## Evidence\n")
        lines.extend(evidence_paths)
        lines.append("")

    return "\n".join(lines)


def _html_status_badge(status: Status) -> str:
    colors = {Status.PASS: "#16a34a", Status.FAIL: "#dc2626", Status.WARNING: "#d97706"}
    labels = {Status.PASS: "PASS", Status.FAIL: "FAIL", Status.WARNING: "WARN"}
    bg = colors.get(status, "#6b7280")
    return f'<span style="background:{bg};color:#fff;padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600">{labels.get(status, status.value.upper())}</span>'


def _html_severity_badge(severity) -> str:
    if severity is None:
        return '<span style="color:#9ca3af">-</span>'
    colors = {"critical": "#dc2626", "major": "#d97706", "minor": "#16a34a"}
    bg = colors.get(severity.value, "#6b7280")
    return f'<span style="background:{bg}22;color:{bg};padding:2px 8px;border-radius:4px;font-size:12px;font-weight:600">{severity.value.capitalize()}</span>'


def _html_cookie_status(cookies: list[CookieInfo], phase: str) -> str:
    tracking = _count_tracking(cookies)
    if phase == "before":
        ok = tracking == 0
        label = "PASS" if ok else "FAIL"
    elif phase == "accept":
        return '<span style="color:#6b7280">Expected</span>'
    elif phase == "reject":
        ok = tracking == 0
        label = "PASS" if ok else "FAIL"
    else:
        return "-"
    color = "#16a34a" if label == "PASS" else "#dc2626"
    return f'<span style="color:{color};font-weight:600">{label}</span>'


def generate_html_report(report: ComplianceReport) -> str:
    """Generate a standalone HTML compliance report."""
    passed = sum(1 for f in report.findings if f.status == Status.PASS)
    total = len(report.findings)

    score_label = report.overall_score.upper()
    score_color = "#d97706"
    if report.overall_score == "pass":
        score_label = "COMPLIANT"
        score_color = "#16a34a"
    elif report.overall_score == "partial":
        score_label = "PARTIAL COMPLIANCE"
        score_color = "#d97706"
    elif report.overall_score == "fail":
        score_label = "NON-COMPLIANT"
        score_color = "#dc2626"
    elif report.overall_score == "pending":
        score_label = "PENDING AI ANALYSIS"
    elif report.overall_score == "not_applicable":
        score_label = "NOT APPLICABLE — NO BANNER DETECTED"
        score_color = "#6b7280"

    # Build findings rows
    findings_rows = ""
    for i, f in enumerate(report.findings, 1):
        fw = f.framework or "-"
        rule = f.rule_id or "-"
        rule_style = 'font-size:12px;color:#6b7280' if rule == "-" else 'font-size:12px;font-weight:600'
        findings_rows += f"""
        <tr>
            <td>{i}</td>
            <td style="white-space:nowrap">{fw}</td>
            <td style="{rule_style};white-space:nowrap">{rule}</td>
            <td>{f.criterion}</td>
            <td>{_html_status_badge(f.status)}</td>
            <td>{_html_severity_badge(f.severity)}</td>
            <td>{f.detail}</td>
        </tr>"""

    # Build cookie rows
    audit = report.cookie_audit
    cookie_rows = ""
    for phase, cookies, phase_key in [
        ("Before consent", audit.cookies_before_consent, "before"),
        ("After accept", audit.cookies_after_accept, "accept"),
        ("After reject", audit.cookies_after_reject, "reject"),
    ]:
        cookie_rows += f"""
        <tr>
            <td>{phase}</td>
            <td>{len(cookies)}</td>
            <td>{_count_tracking(cookies)}</td>
            <td>{_html_cookie_status(cookies, phase_key)}</td>
        </tr>"""

    # Build violations
    violations_html = ""
    if audit.violations:
        items = "".join(f"<li>{v}</li>" for v in audit.violations)
        violations_html = f"""
        <div class="section">
            <h2>Cookie Violations</h2>
            <ul class="violations">{items}</ul>
        </div>"""

    # Build flow results
    flow_html = ""
    if report.flow_results:
        flow_rows = ""
        for fr in report.flow_results:
            result_color = "#16a34a" if fr.passed else "#dc2626"
            result_label = "PASS" if fr.passed else "FAIL"
            flow_rows += f"""
            <tr>
                <td>{fr.action.capitalize()}</td>
                <td>{'Yes' if fr.banner_dismissed else 'No'}</td>
                <td>{'Yes' if fr.tracking_cookies_set else 'No'}</td>
                <td><span style="color:{result_color};font-weight:600">{result_label}</span></td>
            </tr>"""
        flow_html = f"""
        <div class="section">
            <h2>Consent Flow Tests</h2>
            <table>
                <thead><tr><th>Action</th><th>Banner Dismissed</th><th>Tracking Cookies Set</th><th>Result</th></tr></thead>
                <tbody>{flow_rows}</tbody>
            </table>
        </div>"""

    # Build recommendations
    rec_html = ""
    if report.recommendations:
        items = "".join(f"<li>{r}</li>" for r in report.recommendations)
        rec_html = f"""
        <div class="section">
            <h2>Recommendations</h2>
            <ol>{items}</ol>
        </div>"""

    # Build evidence
    evidence_html = ""
    evidence_items = []
    if report.flow_results:
        for fr in report.flow_results:
            if fr.screenshot_path:
                evidence_items.append(f'<li><a href="{fr.screenshot_path}">{fr.action.capitalize()} flow screenshot</a></li>')
    if evidence_items:
        evidence_html = f"""
        <div class="section">
            <h2>Evidence</h2>
            <ul>{"".join(evidence_items)}</ul>
        </div>"""

    today = date.today().isoformat()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Compliance Report — {report.url}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #1e293b; line-height: 1.6; padding: 2rem; }}
    .container {{ max-width: 960px; margin: 0 auto; }}
    .header {{ background: #1e293b; color: #fff; padding: 2rem; border-radius: 12px; margin-bottom: 1.5rem; }}
    .header h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; }}
    .meta {{ display: flex; gap: 2rem; font-size: 0.875rem; color: #94a3b8; margin-top: 0.5rem; }}
    .score-banner {{ background: {score_color}11; border: 2px solid {score_color}; border-radius: 12px; padding: 1.5rem; text-align: center; margin-bottom: 1.5rem; }}
    .score-banner h2 {{ color: {score_color}; font-size: 1.75rem; }}
    .score-banner .detail {{ color: #64748b; margin-top: 0.25rem; }}
    .section {{ background: #fff; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
    .section h2 {{ font-size: 1.125rem; margin-bottom: 1rem; color: #1e293b; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
    th {{ background: #f1f5f9; padding: 0.75rem; text-align: left; font-weight: 600; color: #475569; }}
    td {{ padding: 0.75rem; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    tr:hover {{ background: #f8fafc; }}
    .summary {{ font-size: 0.95rem; color: #475569; }}
    .violations {{ list-style: none; }}
    .violations li {{ background: #fef2f2; border-left: 4px solid #dc2626; padding: 0.75rem 1rem; margin-bottom: 0.5rem; border-radius: 0 6px 6px 0; font-size: 0.875rem; color: #991b1b; }}
    ol, ul {{ padding-left: 1.5rem; }}
    li {{ margin-bottom: 0.5rem; }}
    a {{ color: #2563eb; }}
    .footer {{ text-align: center; font-size: 0.75rem; color: #94a3b8; margin-top: 2rem; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Cookie Consent Compliance Report</h1>
        <div class="meta">
            <span>URL: {report.url}</span>
            <span>Date: {today}</span>
            <span>Agent v{VERSION}</span>
        </div>
    </div>

    <div class="score-banner">
        <h2>{score_label}</h2>
        <div class="detail">{passed}/{total} checks passed</div>
    </div>

    <div class="section">
        <h2>Summary</h2>
        <p class="summary">{report.summary}</p>
    </div>

    <div class="section">
        <h2>Findings</h2>
        <table>
            <thead><tr><th>#</th><th>Framework</th><th>Rule</th><th>Check</th><th>Status</th><th>Severity</th><th>Detail</th></tr></thead>
            <tbody>{findings_rows}</tbody>
        </table>
    </div>

    <div class="section">
        <h2>Cookie Behavior</h2>
        <table>
            <thead><tr><th>Phase</th><th>Cookies Found</th><th>Tracking Cookies</th><th>Status</th></tr></thead>
            <tbody>{cookie_rows}</tbody>
        </table>
    </div>

    {violations_html}
    {flow_html}
    {rec_html}
    {evidence_html}

    <div class="footer">
        Generated by Cookie Consent Compliance QA Agent v{VERSION}
    </div>
</div>
</body>
</html>"""
