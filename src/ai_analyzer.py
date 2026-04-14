import json
import os
from pathlib import Path

import anthropic

from .models import Finding, Status, Severity, BannerDetection, CookieAudit

ANALYSIS_TOOL = {
    "name": "compliance_analysis",
    "description": "Structured GDPR/CCPA cookie consent compliance analysis.",
    "input_schema": {
        "type": "object",
        "properties": {
            "overall_score": {
                "type": "string",
                "enum": ["pass", "partial", "fail"],
                "description": "Overall compliance score.",
            },
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "criterion": {"type": "string"},
                        "status": {"type": "string", "enum": ["pass", "fail", "warning"]},
                        "detail": {"type": "string"},
                        "severity": {
                            "type": "string",
                            "enum": ["critical", "major", "minor"],
                        },
                    },
                    "required": ["criterion", "status", "detail"],
                },
            },
            "summary": {"type": "string"},
            "recommendations": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["overall_score", "findings", "summary", "recommendations"],
    },
}

RESPONSE_SCHEMA = """\
{
  "overall_score": "pass|partial|fail",
  "findings": [
    {
      "criterion": "check name",
      "status": "pass|fail|warning",
      "detail": "explanation",
      "severity": "critical|major|minor"
    }
  ],
  "summary": "one-paragraph summary",
  "recommendations": ["recommendation 1", "recommendation 2"]
}"""


def _format_cookies(cookies) -> str:
    """Format cookie list for the prompt."""
    if not cookies:
        return "None"
    lines = []
    for c in cookies:
        lines.append(f"  - {c.name} (domain: {c.domain}, category: {c.category})")
    return "\n".join(lines)


def build_analysis_prompt(banner: BannerDetection, cookie_audit: CookieAudit) -> str:
    """Build the compliance analysis prompt from collected data."""
    return f"""Analyze this cookie consent banner for GDPR and CCPA compliance.

Banner found: {banner.banner_found}
Banner text: {banner.text or 'N/A'}
Buttons found: {', '.join(banner.buttons) if banner.buttons else 'None'}

Cookies before consent:
{_format_cookies(cookie_audit.cookies_before_consent)}

Cookies after accepting consent:
{_format_cookies(cookie_audit.cookies_after_accept)}

Cookies after rejecting consent:
{_format_cookies(cookie_audit.cookies_after_reject)}

Cookie violations detected: {'; '.join(cookie_audit.violations) if cookie_audit.violations else 'None'}

Evaluate against these criteria:
1. Banner presence — Is a consent banner displayed to the user?
2. Clear explanation — Does the banner clearly explain what cookies are used for?
3. Reject option — Is there a visible "Reject All" or "Decline" button?
4. Equal prominence — Is the reject option equally prominent as accept (no dark patterns)?
5. Pre-consent blocking — Are cookies actually blocked before consent is given?
6. Post-rejection blocking — Does rejecting consent actually prevent tracking cookies?
7. Privacy policy link — Is there a link to the privacy/cookie policy?
8. Clear language — Is the language clear and non-manipulative?

Respond with ONLY a JSON object in this exact format:
{RESPONSE_SCHEMA}"""


def export_for_llm(
    banner: BannerDetection,
    cookie_audit: CookieAudit,
    url: str,
    output_dir: Path | str | None = None,
) -> str:
    """Export collected data as a ready-to-paste LLM prompt file.

    Returns the path to the generated prompt file.
    """
    if output_dir is None:
        from .output import get_output_dir
        output_dir = get_output_dir(url)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    prompt = build_analysis_prompt(banner, cookie_audit)

    # Structured data file (for programmatic use)
    data = {
        "url": url,
        "banner": banner.model_dump(),
        "cookie_audit": cookie_audit.model_dump(),
        "prompt": prompt,
    }
    data_path = output_dir / "analysis-input.json"
    data_path.write_text(json.dumps(data, indent=2))

    # Ready-to-paste prompt file (for any LLM)
    prompt_path = output_dir / "analysis-prompt.md"
    analysis_result_path = output_dir / "analysis-result.json"
    prompt_content = f"""# Cookie Consent Compliance Analysis

Paste this entire prompt into any LLM (ChatGPT, Claude, Gemini, etc.) to get the compliance analysis.
Save the JSON response as `{analysis_result_path}`, then re-run:

```
python -m src.main audit {url} --analysis {analysis_result_path}
```

---

{prompt}
"""
    prompt_path.write_text(prompt_content)

    return str(prompt_path)


def parse_analysis_result(result_path: str) -> tuple[str, list[Finding], str, list[str]]:
    """Parse a compliance analysis result from a JSON file.

    Accepts the JSON file produced by an LLM from the exported prompt.
    """
    path = Path(result_path)
    if not path.exists():
        prompt_path = path.parent / "analysis-prompt.md"
        raise FileNotFoundError(
            f"Analysis file not found: {result_path}\n\n"
            f"This file must be created first. Two options:\n"
            f"  1. Paste the prompt from {prompt_path} into any LLM and save the JSON response as {result_path}\n"
            f"  2. In Claude Code, ask Claude to read {path.parent / 'analysis-input.json'} and generate the analysis"
        )
    text = path.read_text()

    # Handle cases where the JSON is wrapped in markdown code blocks
    if "```" in text:
        start = text.index("```")
        # Skip the opening ``` and optional language tag
        start = text.index("\n", start) + 1
        end = text.index("```", start)
        text = text[start:end].strip()

    # Extract JSON if there's surrounding text
    try:
        brace_start = text.index("{")
        brace_end = text.rindex("}") + 1
        text = text[brace_start:brace_end]
    except ValueError:
        pass

    data = json.loads(text)
    return _parse_analysis_data(data)


def _parse_analysis_data(data: dict) -> tuple[str, list[Finding], str, list[str]]:
    """Parse the analysis dict into typed results."""
    findings = []
    for f in data.get("findings", []):
        severity = f.get("severity")
        findings.append(
            Finding(
                criterion=f["criterion"],
                status=Status(f["status"]),
                detail=f["detail"],
                severity=Severity(severity) if severity else None,
                framework=f.get("framework", "GDPR/CCPA"),
                rule_id=f.get("rule_id"),
            )
        )

    return (
        data.get("overall_score", "fail"),
        findings,
        data.get("summary", ""),
        data.get("recommendations", []),
    )


def analyze_compliance(
    banner: BannerDetection,
    cookie_audit: CookieAudit,
) -> tuple[str, list[Finding], str, list[str]]:
    """Use Claude API to analyze banner compliance against GDPR/CCPA criteria.

    Returns (overall_score, findings, summary, recommendations).
    """
    prompt = build_analysis_prompt(banner, cookie_audit)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return (
            "pending",
            [],
            "AI analysis requires an API key or manual LLM analysis. "
            "Run with --export to generate a prompt file.",
            [],
        )

    client = anthropic.Anthropic(api_key=api_key)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            tools=[ANALYSIS_TOOL],
            tool_choice={"type": "tool", "name": "compliance_analysis"},
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        return "fail", [], f"AI analysis failed: {e}", []

    # Extract tool use result
    tool_input = None
    for block in response.content:
        if block.type == "tool_use":
            tool_input = block.input
            break

    if tool_input is None:
        return "fail", [], "Analysis failed — no structured output returned.", []

    return _parse_analysis_data(tool_input)
