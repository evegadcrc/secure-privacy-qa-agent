# Cookie Consent Compliance QA Agent

An AI-powered agent that audits any website's cookie consent banner for GDPR/CCPA compliance. Built with Playwright for browser automation and Claude API for intelligent compliance analysis.

## What It Does

Three modes of operation:

1. **`audit`** — Automated scan: detects banner, tests consent flows, inspects cookies, runs AI analysis, generates compliance reports (Markdown + HTML)
2. **`assisted`** — Interactive guided testing: opens a headed browser and walks you through 41 compliance checks across 7 frameworks, capturing evidence as you go
3. **`generate-tests`** — Test plan generator: scans the site and produces an Excel workbook with manual test cases tailored to what was found

## Compliance Frameworks

Covers **41 checks** across 7 regulatory frameworks:

| Framework | Checks | Focus |
|-----------|--------|-------|
| **GDPR** | 7 | Lawful basis, consent quality, granularity, withdrawal, accountability |
| **ePrivacy** | 4 | Cookie consent, transparency, exemptions, third-party disclosure |
| **EDPB** | 5 | Pre-ticked boxes, scrolling ≠ consent, cookie walls, withdrawal parity |
| **Planet49** | 4 | Active opt-in, cookie duration, third-party access, separate consent |
| **CNIL** | 5 | Equal reject/accept, cookie walls, 13-month consent, change choices |
| **ICO** | 6 | Strictly necessary exemption, positive action, granular choices, refresh |
| **WCAG 2.2 AA** | 10 | Keyboard access, focus management, contrast, target size, screen reader, reflow |

## Architecture

```
                    +------------------+
                    |   CLI Entrypoint |
                    |  audit | assisted|
                    |  generate-tests  |
                    +--------+---------+
                             |
                    +--------v---------+
                    |  Banner Detector |
                    |   (Playwright)   |
                    +--------+---------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v---+  +------v------+  +----v--------+
     | UI Analyzer |  | Flow Tester |  | Cookie      |
     | (Claude AI) |  | (Playwright)|  | Inspector   |
     +--------+---+  +------+------+  +----+--------+
              |              |              |
              +--------------+--------------+
                             |
              +--------------+--------------+
              |              |              |
     +--------v---------+ +-v-----------+ +v-----------+
     | Report Generator | | Assisted    | | Test Case  |
     | (MD + HTML)      | | Testing     | | Generator  |
     +------------------+ | (Interactive)| | (Excel)   |
                          +-------------+ +------------+
```

## Setup

```bash
# Clone and set up
git clone https://github.com/evegacrc/consent-qa-agent.git
cd consent-qa-agent

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium

# Optional: set API key for AI-powered analysis
cp .env.example .env
# Edit .env: ANTHROPIC_API_KEY=sk-ant-...
```

## Usage

### Automated Audit (`audit`)

Scans a site, detects the consent banner, tests accept/reject/close flows, inspects cookies, and generates a compliance report. Optionally runs automated framework checks (WCAG, GDPR, CNIL, etc.).

```bash
# Basic audit — results go to output/secureprivacy.ai/
python -m src.main audit https://secureprivacy.ai

# Run with WCAG accessibility checks
python -m src.main audit https://secureprivacy.ai -f WCAG

# Run with multiple framework checks
python -m src.main audit https://secureprivacy.ai -f WCAG,GDPR,CNIL

# All frameworks automated checks
python -m src.main audit https://secureprivacy.ai -f GDPR,ePrivacy,EDPB,Planet49,CNIL,ICO,WCAG -v

# Verbose mode — see detailed progress
python -m src.main audit https://secureprivacy.ai -v

# Custom output path for the report
python -m src.main audit https://secureprivacy.ai -o my-report.md

# Run with visible browser (headed mode)
python -m src.main audit https://secureprivacy.ai --headed

# Import analysis from an external LLM (no API key needed)
python -m src.main audit https://secureprivacy.ai --analysis output/secureprivacy.ai/analysis-result.json
```

| Option | Description |
|--------|-------------|
| `URL` | Target website to audit (required) |
| `-f, --frameworks` | Run automated framework checks: `GDPR`, `ePrivacy`, `EDPB`, `Planet49`, `CNIL`, `ICO`, `WCAG` (comma-separated, default: none) |
| `-o, --output` | Report file path (default: `output/{domain}/report.md`) |
| `-v, --verbose` | Show detailed progress in terminal |
| `--headless/--headed` | Browser visibility (default: headless) |
| `-a, --analysis` | Import analysis from a JSON file (skip API call) |

When `-f` is provided, the audit runs the automatable subset of those frameworks using Playwright (keyboard navigation, focus detection, ARIA attributes, target size measurement, pre-consent cookie checks, reject button detection, etc.) and merges the findings into the report alongside the AI analysis.

**Output files** (all in `output/{domain}/`):
```
output/secureprivacy.ai/
  report.md                # Markdown report
  report.html              # Standalone HTML report (opens in any browser)
  screenshots/
    banner.png             # Captured consent banner
    after-accept.png       # State after clicking Accept
    after-reject.png       # State after clicking Reject
```

**Without an API key**, the audit exports files for external LLM analysis:
```
output/secureprivacy.ai/
  analysis-input.json      # Structured scan data
  analysis-prompt.md       # Ready-to-paste prompt for any LLM
```
Paste the prompt into ChatGPT/Claude/Gemini, save the JSON response as `analysis-result.json` in the same directory, then re-run:
```bash
python -m src.main audit https://secureprivacy.ai --analysis output/secureprivacy.ai/analysis-result.json
```

## Utils

The framework includes two utilities built on top of the core scanner. Both use the shared compliance knowledge base in `src/utils/compliance_frameworks.py` (41 checks, 7 frameworks) and produce output under `output/{domain}/`.

| Utility | Command | Purpose |
|---------|---------|---------|
| **Assisted Testing** | `assisted` | Interactive Playwright-guided session — opens a headed browser, walks you through each check, captures evidence, records results |
| **Test Case Generator** | `generate-tests` | Scans the site, then generates a contextualized Excel workbook with manual test cases for a QA team to execute offline |

### 1. Assisted Manual Testing (`assisted`)

Opens a headed browser and walks you through compliance checks step-by-step. Works like `playwright codegen` but focused on consent compliance verification across 7 regulatory frameworks.

```bash
# Run all 41 checks across all 7 frameworks
python -m src.main assisted https://secureprivacy.ai

# Test only specific frameworks
python -m src.main assisted https://secureprivacy.ai -f GDPR,CNIL

# Test a single framework
python -m src.main assisted https://secureprivacy.ai -f ICO

# Custom output directory
python -m src.main assisted https://secureprivacy.ai -o my-session/
```

| Option | Description |
|--------|-------------|
| `URL` | Target website (required) |
| `-f, --frameworks` | Comma-separated list: `GDPR`, `ePrivacy`, `EDPB`, `Planet49`, `CNIL`, `ICO`, `WCAG` (default: all) |
| `-o, --output-dir` | Directory for results (default: `output/{domain}/assisted/`) |

**What happens during a session:**
1. A Chromium browser opens in headed mode (you can see and interact with it)
2. For each compliance check, the terminal shows:
   - The check ID, framework, title, severity, and regulation reference
   - Step-by-step instructions to follow in the browser
   - Expected result for a compliant site
   - Automated pre-check hints (e.g., "SCAN: 2 tracking cookies found before consent")
3. You interact with the browser to perform the check
4. You record your result: **p**=Pass, **f**=Fail, **w**=Warning, **s**=Skip, **n/a**=Not Applicable
5. Optional notes for each check
6. Between checks that need a fresh session, cookies are cleared automatically
7. Press `Ctrl+C` at any time to end early (results are saved)

**Example session flow:**
```
─────────────────── Check 1/31 ────────────────────
╭─ GDPR — GDPR-001 ───────────────────────────────╮
│ Prior consent before non-essential cookies        │
│ No analytics, marketing, or tracking cookies may  │
│ be set before the user gives explicit consent.    │
│                                                   │
│ Severity: CRITICAL  |  Reference: GDPR Art. 6(1) │
╰──────────────────────────────────────────────────╯

Steps to execute:
  1. Open the site in a fresh browser
  2. Before interacting with the banner, check cookies
  3. List all cookies present
  4. Verify only strictly necessary cookies are set

Expected result: Zero analytics/marketing/tracking cookies

AUTO-DETECT: 2 tracking cookie(s) found before consent: _gcl_au, test_cookie

Result [p/f/w/s/n/a]: f
Notes: _gcl_au and test_cookie present before any consent
```

**Output files:**
```
output/secureprivacy.ai/assisted/
  session-results.json     # Full results with browser state snapshots
  assisted-report.md       # Markdown summary grouped by framework
  screenshots/
    GDPR-001.png           # Screenshot per check
    GDPR-001-after.png     # After user interaction
    ...
```

### 2. Test Case Generator (`generate-tests`)

Scans the site to gather context (banner detection, cookie inventory), then generates a tailored Excel workbook with manual test cases organized by compliance framework.

```bash
# Generate test cases for all 7 frameworks
python -m src.main generate-tests https://secureprivacy.ai

# Generate for specific frameworks only
python -m src.main generate-tests https://secureprivacy.ai -f GDPR,CNIL,ICO

# Custom output path
python -m src.main generate-tests https://secureprivacy.ai -o my-tests.xlsx

# Test a different site — output goes to its own directory
python -m src.main generate-tests https://stackoverflow.com
```

| Option | Description |
|--------|-------------|
| `URL` | Target website (required) |
| `-f, --frameworks` | Comma-separated list: `GDPR`, `ePrivacy`, `EDPB`, `Planet49`, `CNIL`, `ICO`, `WCAG` (default: all) |
| `-o, --output` | Excel file path (default: `output/{domain}/compliance-tests.xlsx`) |

**What the Excel contains:**

The workbook has 8 sheets:

| Sheet | Contents |
|-------|----------|
| **Overview** | Target URL, scan date, banner status, pre-consent cookies found, tracking alerts, framework summary table, instructions |
| **GDPR** | 7 test cases covering lawful basis, consent quality, withdrawal |
| **ePrivacy** | 4 test cases covering cookie consent, transparency, exemptions |
| **EDPB** | 5 test cases covering valid consent guidelines |
| **Planet49** | 4 test cases covering the CJEU ruling requirements |
| **CNIL** | 5 test cases covering French DPA requirements |
| **ICO** | 6 test cases covering UK ICO guidance |
| **WCAG** | 10 test cases covering banner accessibility (keyboard, focus, contrast, target size, screen reader) |

Each test case row has 15 columns:

| Column | Pre-filled? | Description |
|--------|------------|-------------|
| ID | Yes | Unique check ID (e.g., `GDPR-001`) |
| Category | Yes | Logical grouping (e.g., "Lawful Basis") |
| Check | Yes | Short check title |
| Severity | Yes | CRITICAL / MAJOR / MINOR (color-coded) |
| Description | Yes | What to verify and why |
| Precondition | Yes | Setup needed (e.g., "Fresh browser session") |
| Test Steps | Yes | Numbered steps to follow |
| Expected Result | Yes | What compliance looks like |
| Automated? | Yes | Whether the scanner can partially verify this |
| Site Context | Yes | Pre-scan findings (e.g., "SCAN: 2 tracking cookies before consent: _gcl_au, test_cookie") |
| Actual Result | No | For the tester to fill in |
| Status | No | Dropdown: PASS / FAIL / WARNING / SKIP / N/A |
| Tester | No | Name of the person testing |
| Date | No | When the test was performed |
| Notes | No | Additional observations |

## Output Directory Structure

All output is organized by domain under `output/`:

```
output/
  secureprivacy.ai/
    report.md                  # Markdown compliance report
    report.html                # HTML compliance report
    compliance-tests.xlsx      # Excel test plan
    analysis-input.json        # Scan data for LLM analysis
    analysis-prompt.md         # Ready-to-paste LLM prompt
    analysis-result.json       # LLM analysis results
    screenshots/
      banner.png
      after-accept.png
      after-reject.png
    assisted/
      session-results.json
      assisted-report.md
      screenshots/
        GDPR-001.png
        ...
  stackoverflow.com/           # Each site gets its own directory
    report.md
    report.html
    ...
```

## Example Output

### Automated Audit Report (Markdown)
```
## Overall Score: PARTIAL COMPLIANCE (5/8 checks passed)

| # | Check | Status | Severity | Detail |
|---|-------|--------|----------|--------|
| 1 | Banner presence | PASS | Minor | Consent banner displayed via iframe CMP |
| 2 | Clear explanation | WARN | Minor | Mentions cookies but no category details |
| 3 | Reject option | PASS | - | 'Decline' button visible alongside 'Accept all' |
| 5 | Pre-consent blocking | FAIL | Critical | _gcl_au and test_cookie set before consent |
```

### HTML Report
A standalone styled HTML page with color-coded score banner, findings table with status badges, cookie behavior analysis, and recommendations. Opens directly in any browser.

### Excel Test Plan
8 sheets (Overview + 7 frameworks), 41 test cases, severity color-coding, status dropdowns, pre-populated site context from the automated scan.

## Tech Stack

- **Python 3.11+**
- **Playwright** (async, Chromium) — browser automation
- **Anthropic Claude API** (claude-sonnet-4-20250514) — AI analysis + vision
- **Click** — CLI framework with subcommands
- **Rich** — terminal output and interactive prompts
- **Pydantic** — data validation
- **openpyxl** — Excel workbook generation

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
secure-privacy-qa-agent/
  README.md
  requirements.txt
  pyproject.toml
  .env.example
  src/
    main.py               # CLI entrypoint (audit, assisted, generate-tests)
    banner_detector.py     # Playwright: find & capture consent banner
    flow_tester.py         # Playwright: test accept/reject/close flows
    cookie_inspector.py    # Playwright: check cookies before/after consent
    ai_analyzer.py         # Claude API: analyze banner compliance
    report_generator.py    # Markdown + HTML report generation
    output.py              # Output directory management (output/{domain}/)
    models.py              # Pydantic models for findings
    utils/
      compliance_frameworks.py  # 41 checks across 7 regulatory frameworks
      assisted_testing.py       # Interactive Playwright-guided manual testing
      test_case_generator.py    # Excel test case generator
  tests/
    test_banner_detector.py
    test_flow_tester.py
    test_cookie_inspector.py
  output/                  # Generated output (gitignored)
    {domain}/
      report.md
      report.html
      compliance-tests.xlsx
      screenshots/
      assisted/
  examples/
    report-secureprivacy.md
```

## License

MIT
