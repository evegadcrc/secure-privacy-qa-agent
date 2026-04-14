"""Compliance check definitions for cookie consent across 7 regulatory frameworks.

Each check is a dict with:
    id          — Unique identifier (FRAMEWORK-NNN)
    framework   — Regulatory source
    category    — Logical grouping within the framework
    title       — Short human-readable check name
    description — What to verify and why
    steps       — Ordered list of manual test steps
    expected    — What a compliant result looks like
    severity    — critical / major / minor
    automated   — Whether the automated scanner can cover this check
    references  — Regulation article or guideline section
"""

from dataclasses import dataclass, field


@dataclass
class ComplianceCheck:
    id: str
    framework: str
    category: str
    title: str
    description: str
    steps: list[str]
    expected: str
    severity: str  # critical, major, minor
    automated: bool = False
    references: str = ""


# ---------------------------------------------------------------------------
# GDPR — General Data Protection Regulation
# ---------------------------------------------------------------------------
GDPR_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="GDPR-001",
        framework="GDPR",
        category="Lawful Basis",
        title="Prior consent before non-essential cookies",
        description="No analytics, marketing, or tracking cookies may be set before the user gives explicit consent.",
        steps=[
            "Open the site in a fresh browser (clear all cookies/storage first).",
            "Before interacting with the consent banner, open DevTools → Application → Cookies.",
            "List all cookies present. Identify any that are non-essential (analytics, marketing, tracking).",
            "Verify that only strictly necessary cookies (session, CSRF, load balancer) are set.",
        ],
        expected="Zero analytics/marketing/tracking cookies before any user interaction with the consent banner.",
        severity="critical",
        automated=True,
        references="GDPR Art. 6(1)(a), Recital 32; ePrivacy Art. 5(3)",
    ),
    ComplianceCheck(
        id="GDPR-002",
        framework="GDPR",
        category="Consent Quality",
        title="Freely given consent — no cookie walls",
        description="Access to the site must not be conditional on accepting cookies. Cookie walls that block content until consent is given are generally non-compliant.",
        steps=[
            "Navigate to the site with a fresh session.",
            "Attempt to scroll, navigate, or interact with the site WITHOUT accepting cookies.",
            "Check if content is blocked, blurred, or hidden behind an overlay.",
            "Verify the site is usable without giving consent.",
        ],
        expected="Full site content is accessible without accepting cookies. No blocking overlay or paywall.",
        severity="critical",
        references="GDPR Art. 7(4), EDPB Guidelines 05/2020 §39",
    ),
    ComplianceCheck(
        id="GDPR-003",
        framework="GDPR",
        category="Consent Quality",
        title="Specific and informed consent",
        description="The consent banner must clearly state what cookies are used for and for what purposes.",
        steps=[
            "Read the consent banner text.",
            "Check if it mentions specific purposes (analytics, marketing, personalization).",
            "Verify the information is in plain language, not legal jargon.",
            "Check if a link to a detailed cookie/privacy policy is provided.",
        ],
        expected="Banner explains cookie purposes clearly. Link to full cookie policy is present.",
        severity="major",
        references="GDPR Art. 13, 14; Recital 42",
    ),
    ComplianceCheck(
        id="GDPR-004",
        framework="GDPR",
        category="Consent Quality",
        title="Unambiguous active opt-in",
        description="Consent must require a clear affirmative action. Pre-ticked boxes, silence, or inactivity do not constitute consent.",
        steps=[
            "Inspect the consent banner or preference center.",
            "Check if any cookie categories are pre-selected or pre-ticked.",
            "Verify that accepting requires clicking a button (not just scrolling or navigating).",
            "If there's a preference center, confirm all non-essential categories start unchecked.",
        ],
        expected="No pre-ticked checkboxes. Consent requires explicit click. Non-essential categories default to OFF.",
        severity="critical",
        references="GDPR Art. 4(11), Recital 32; Planet49 CJEU C-673/17",
    ),
    ComplianceCheck(
        id="GDPR-005",
        framework="GDPR",
        category="Consent Quality",
        title="Granular consent per purpose",
        description="Users must be able to consent to different cookie purposes independently (analytics vs marketing vs functional).",
        steps=[
            "Open the consent preference center (click 'Manage Preferences', 'Customize', or similar).",
            "Check if individual cookie categories can be toggled independently.",
            "Verify categories are clearly labeled (e.g., 'Analytics', 'Marketing', 'Functional').",
            "Confirm that accepting one category does not auto-accept others.",
        ],
        expected="Preference center allows per-category control. Each category has its own toggle.",
        severity="major",
        references="GDPR Recital 43; EDPB Guidelines 05/2020 §43",
    ),
    ComplianceCheck(
        id="GDPR-006",
        framework="GDPR",
        category="Withdrawal",
        title="Easy withdrawal of consent",
        description="It must be as easy to withdraw consent as it is to give it. A persistent mechanism to change cookie preferences must be available.",
        steps=[
            "Accept all cookies via the banner.",
            "After the banner is dismissed, look for a way to change cookie preferences.",
            "Check for: a persistent cookie icon/button, a link in the footer, or a settings page.",
            "Click the mechanism and verify you can revoke consent for specific categories.",
            "After revoking, verify tracking cookies are removed.",
        ],
        expected="A visible, easily accessible mechanism to revoke consent exists. Revoking removes non-essential cookies.",
        severity="major",
        references="GDPR Art. 7(3); EDPB Guidelines 05/2020 §113",
    ),
    ComplianceCheck(
        id="GDPR-007",
        framework="GDPR",
        category="Accountability",
        title="Proof of consent",
        description="The data controller must be able to demonstrate that the user consented. Consent records must be maintained.",
        steps=[
            "Accept cookies on the consent banner.",
            "Open DevTools → Application → Cookies and Local Storage.",
            "Look for a consent record cookie (e.g., 'CookieConsent', 'OptanonConsent', 'euconsent-v2').",
            "Check its value — it should encode what was consented to and when.",
            "Verify the consent cookie has a reasonable expiry (not infinite).",
        ],
        expected="A consent record cookie exists encoding user choices. It has a defined expiry.",
        severity="major",
        references="GDPR Art. 7(1); EDPB Guidelines 05/2020 §108",
    ),
]

# ---------------------------------------------------------------------------
# ePrivacy Directive — Article 5(3) (Cookie Law)
# ---------------------------------------------------------------------------
EPRIVACY_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="EPRIV-001",
        framework="ePrivacy",
        category="Cookie Consent",
        title="Consent before storing non-essential cookies",
        description="Under the ePrivacy Directive, storing information on a user's device requires prior consent, except for strictly necessary cookies.",
        steps=[
            "Open the site in a fresh session.",
            "Before interacting with the banner, check DevTools → Application → Cookies.",
            "Identify all cookies. Classify as strictly necessary or non-essential.",
            "Verify no non-essential cookies are present before consent.",
        ],
        expected="Only strictly necessary cookies present before consent.",
        severity="critical",
        automated=True,
        references="ePrivacy Directive Art. 5(3)",
    ),
    ComplianceCheck(
        id="EPRIV-002",
        framework="ePrivacy",
        category="Transparency",
        title="Clear and comprehensive information about cookies",
        description="Users must be provided with clear and comprehensive information about the purposes of cookie storage.",
        steps=[
            "Read the consent banner text.",
            "Navigate to the cookie policy or details page.",
            "Check if every cookie is listed with: name, purpose, duration, and provider.",
            "Verify third-party cookies are disclosed with the third party named.",
        ],
        expected="Cookie policy lists all cookies with name, purpose, duration, and provider. Third parties identified.",
        severity="major",
        references="ePrivacy Directive Art. 5(3); GDPR Art. 13",
    ),
    ComplianceCheck(
        id="EPRIV-003",
        framework="ePrivacy",
        category="Exemptions",
        title="Strictly necessary cookie exemption correctly applied",
        description="Only cookies that are genuinely necessary for the service requested by the user are exempt from consent. This must not be abused.",
        steps=[
            "Identify all cookies classified as 'strictly necessary' by the site.",
            "For each, verify it serves a legitimate necessary purpose (session, auth, security, load balancing).",
            "Check that analytics, preferences remembered across sessions, or marketing cookies are NOT classified as necessary.",
        ],
        expected="Only genuine session/auth/security cookies are classified as strictly necessary. No analytics or marketing cookies exempted.",
        severity="critical",
        references="ePrivacy Directive Art. 5(3); EDPB Guidelines 2/2023",
    ),
    ComplianceCheck(
        id="EPRIV-004",
        framework="ePrivacy",
        category="Third Parties",
        title="Third-party cookie disclosure",
        description="If third-party cookies are set (e.g., Google, Facebook), users must be informed about which third parties receive data.",
        steps=[
            "Accept all cookies.",
            "In DevTools, filter cookies by third-party domains.",
            "Check if the cookie policy names these third parties explicitly.",
            "Verify the purposes for each third-party cookie are explained.",
        ],
        expected="All third-party cookie providers are named in the cookie policy with their purposes.",
        severity="major",
        automated=True,
        references="ePrivacy Directive Art. 5(3); GDPR Art. 13(1)(e)",
    ),
]

# ---------------------------------------------------------------------------
# EDPB Guidelines 05/2020 on Consent
# ---------------------------------------------------------------------------
EDPB_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="EDPB-001",
        framework="EDPB",
        category="Valid Consent",
        title="No pre-ticked boxes",
        description="Pre-ticked checkboxes do not constitute valid consent under the EDPB guidelines.",
        steps=[
            "Open the consent preference center.",
            "Inspect all checkboxes and toggles.",
            "Verify all non-essential categories are unchecked/off by default.",
            "Take a screenshot of the default state for evidence.",
        ],
        expected="All non-essential cookie categories default to unchecked/off.",
        severity="critical",
        references="EDPB Guidelines 05/2020 §79; Planet49 CJEU C-673/17",
    ),
    ComplianceCheck(
        id="EDPB-002",
        framework="EDPB",
        category="Valid Consent",
        title="Scrolling or continued browsing is NOT valid consent",
        description="The EDPB explicitly states that scrolling through a page or continuing to browse does not meet the threshold for valid consent.",
        steps=[
            "Open the site and note the consent banner.",
            "Without clicking any button, scroll down through the page.",
            "After scrolling, check if the banner is still present.",
            "Check cookies — verify no new non-essential cookies were set by scrolling alone.",
            "Navigate to another page on the site. Verify the banner reappears if consent wasn't given.",
        ],
        expected="Scrolling does not dismiss the banner or set non-essential cookies. Banner persists until explicit action.",
        severity="critical",
        references="EDPB Guidelines 05/2020 §86",
    ),
    ComplianceCheck(
        id="EDPB-003",
        framework="EDPB",
        category="Equal Choice",
        title="Withdrawal as easy as giving consent",
        description="It must be as easy to withdraw consent as to give it. If consent is one click, withdrawal must also be one click.",
        steps=[
            "Count the clicks needed to accept all cookies (usually 1 click on 'Accept All').",
            "Accept cookies, then find the mechanism to change your preferences.",
            "Count the clicks needed to revoke consent.",
            "Compare: withdrawal should require the same or fewer steps than giving consent.",
        ],
        expected="Revoking consent requires the same number of clicks (or fewer) as giving consent.",
        severity="major",
        references="EDPB Guidelines 05/2020 §113; GDPR Art. 7(3)",
    ),
    ComplianceCheck(
        id="EDPB-004",
        framework="EDPB",
        category="Bundled Consent",
        title="No bundled consent with terms of service",
        description="Consent for cookies must not be bundled with acceptance of terms of service or other agreements.",
        steps=[
            "Check if the consent banner combines cookie consent with T&C or account registration.",
            "Verify that accepting cookies is a separate action from any other agreement.",
            "If there's a signup form, confirm cookie consent is a separate checkbox.",
        ],
        expected="Cookie consent is a standalone action, not bundled with T&C or other agreements.",
        severity="major",
        references="EDPB Guidelines 05/2020 §41; GDPR Art. 7(2)",
    ),
    ComplianceCheck(
        id="EDPB-005",
        framework="EDPB",
        category="Consent Refresh",
        title="Re-consent at appropriate intervals",
        description="Consent should be refreshed at appropriate intervals. Perpetual consent is not appropriate.",
        steps=[
            "Accept cookies and find the consent record cookie.",
            "Check its expiry date.",
            "Verify the expiry is reasonable (6-13 months is typical).",
            "Check if the banner reappears after the consent cookie expires.",
        ],
        expected="Consent cookie expires within 13 months. Banner reappears when consent expires.",
        severity="minor",
        references="EDPB Guidelines 05/2020 §109",
    ),
]

# ---------------------------------------------------------------------------
# Planet49 — CJEU Ruling C-673/17
# ---------------------------------------------------------------------------
PLANET49_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="P49-001",
        framework="Planet49",
        category="Active Consent",
        title="Active opt-in required — no pre-checked boxes",
        description="The Planet49 ruling confirmed that pre-checked checkboxes do not constitute valid consent for cookies.",
        steps=[
            "Open the consent preference center.",
            "Screenshot the initial state of all checkboxes/toggles.",
            "Verify every non-essential category is unchecked by default.",
            "Confirm the user must take positive action to enable each category.",
        ],
        expected="All non-essential cookie categories require active opt-in. No pre-checked boxes.",
        severity="critical",
        references="CJEU C-673/17 Planet49, para. 63",
    ),
    ComplianceCheck(
        id="P49-002",
        framework="Planet49",
        category="Transparency",
        title="Information about cookie duration",
        description="Users must be informed about how long cookies will be stored on their device.",
        steps=[
            "Open the cookie policy or preference center.",
            "For each cookie listed, check if the duration/expiry is specified.",
            "Verify both session cookies and persistent cookies show their duration.",
        ],
        expected="Cookie policy or preference center shows duration for each cookie.",
        severity="major",
        references="CJEU C-673/17 Planet49, para. 81",
    ),
    ComplianceCheck(
        id="P49-003",
        framework="Planet49",
        category="Transparency",
        title="Information about third-party access",
        description="Users must be told whether third parties have access to the cookies.",
        steps=[
            "Review the cookie policy.",
            "For cookies set by third parties, verify the third party is named.",
            "Check if the policy explains what data third parties receive.",
        ],
        expected="Third-party cookie providers are named with description of data they receive.",
        severity="major",
        references="CJEU C-673/17 Planet49, para. 81",
    ),
    ComplianceCheck(
        id="P49-004",
        framework="Planet49",
        category="Separate Consent",
        title="Consent separate from other declarations",
        description="Cookie consent must be separate from consent for other purposes (e.g., newsletter signup, T&C acceptance).",
        steps=[
            "Check if the cookie consent is embedded within any other form or agreement.",
            "Verify the consent banner is a standalone UI element.",
            "If forms exist on the page, confirm cookie consent is not a prerequisite.",
        ],
        expected="Cookie consent is a standalone mechanism, not embedded in or required by other forms.",
        severity="major",
        references="CJEU C-673/17 Planet49; GDPR Art. 7(2)",
    ),
]

# ---------------------------------------------------------------------------
# CNIL — French Data Protection Authority Guidelines (2020)
# ---------------------------------------------------------------------------
CNIL_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="CNIL-001",
        framework="CNIL",
        category="Equal Choice",
        title="Reject as easy as accept — same level, same prominence",
        description="CNIL requires that refusing cookies must be as simple as accepting them. The reject button must be on the same level (first screen) and with equal visual weight.",
        steps=[
            "Open the site and view the consent banner.",
            "Verify a 'Reject' or 'Decline' button is visible on the FIRST screen (not hidden behind 'Settings').",
            "Compare the visual weight of 'Accept' vs 'Reject' (size, color, contrast, position).",
            "If 'Reject' is less prominent, note the specific difference.",
        ],
        expected="'Reject All' is on the same screen as 'Accept All' with equal size, color, and visual weight.",
        severity="critical",
        automated=True,
        references="CNIL Guidelines 2020, §2.2; Deliberation 2020-091",
    ),
    ComplianceCheck(
        id="CNIL-002",
        framework="CNIL",
        category="Cookie Walls",
        title="No cookie walls",
        description="CNIL considers cookie walls (blocking access unless cookies are accepted) as generally non-compliant.",
        steps=[
            "Navigate to the site without accepting cookies.",
            "Attempt to browse content, click links, and use site features.",
            "Check for any overlay or blocker preventing access.",
            "Verify content is not blurred, locked, or degraded.",
        ],
        expected="Full site access without cookie consent. No content blocking or degradation.",
        severity="critical",
        references="CNIL Guidelines 2020, §2.1",
    ),
    ComplianceCheck(
        id="CNIL-003",
        framework="CNIL",
        category="Consent Duration",
        title="Consent valid for maximum 13 months",
        description="CNIL specifies that consent should be valid for a maximum of 13 months before requiring re-consent.",
        steps=[
            "Accept all cookies.",
            "Find the consent record cookie in DevTools.",
            "Check its expiry date.",
            "Calculate the duration — it must not exceed 13 months from the date it was set.",
        ],
        expected="Consent cookie expiry is 13 months or less from creation date.",
        severity="major",
        references="CNIL Guidelines 2020, §3.1; Deliberation 2020-091",
    ),
    ComplianceCheck(
        id="CNIL-004",
        framework="CNIL",
        category="Valid Consent",
        title="Continuing to browse is NOT valid consent",
        description="CNIL explicitly states that simply continuing to navigate the site does not constitute consent.",
        steps=[
            "Open the site and observe the consent banner.",
            "Without interacting with the banner, navigate to 2-3 other pages on the site.",
            "After each navigation, check if new non-essential cookies were set.",
            "Verify the banner continues to appear on each page.",
        ],
        expected="No non-essential cookies set by navigation alone. Banner persists across pages until explicit consent.",
        severity="critical",
        references="CNIL Guidelines 2020, §2.3",
    ),
    ComplianceCheck(
        id="CNIL-005",
        framework="CNIL",
        category="Withdrawal",
        title="Ability to change choices at any time",
        description="Users must be able to modify their consent choices at any time through an easily accessible mechanism.",
        steps=[
            "Accept all cookies and dismiss the banner.",
            "Look for a persistent mechanism to change choices (footer link, floating icon, settings page).",
            "Click the mechanism and verify you can toggle individual categories.",
            "Save new preferences and verify cookies are updated accordingly.",
        ],
        expected="A visible mechanism exists to modify consent. Changes take effect immediately (cookies removed/added).",
        severity="major",
        references="CNIL Guidelines 2020, §3.2",
    ),
]

# ---------------------------------------------------------------------------
# ICO — UK Information Commissioner's Office Guidance
# ---------------------------------------------------------------------------
ICO_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="ICO-001",
        framework="ICO",
        category="Exemptions",
        title="Strictly necessary cookies correctly identified",
        description="ICO guidance states that only cookies essential for the service explicitly requested by the user are exempt from consent.",
        steps=[
            "Navigate to the site and identify all cookies set without consent.",
            "For each pre-consent cookie, verify it serves a strictly necessary purpose:",
            "  - Session management, authentication, security (CSRF), load balancing are necessary.",
            "  - Analytics, preferences, marketing, social media are NOT necessary.",
            "Cross-reference with the site's cookie policy classification.",
        ],
        expected="Only genuinely necessary cookies are set without consent. No analytics or marketing cookies misclassified.",
        severity="critical",
        automated=True,
        references="ICO Cookie Guidance, 'What are strictly necessary cookies?'",
    ),
    ComplianceCheck(
        id="ICO-002",
        framework="ICO",
        category="Transparency",
        title="Clear information about what each cookie does",
        description="Users must be told clearly what each cookie does, in language they can understand.",
        steps=[
            "Open the cookie policy or preference center.",
            "For each cookie, verify: name, purpose, category, expiry, and provider are listed.",
            "Check that descriptions are in plain language (not just technical names).",
            "Verify the information is up to date and matches actual cookies being set.",
        ],
        expected="Complete cookie inventory with plain-language descriptions. All active cookies are listed.",
        severity="major",
        references="ICO Cookie Guidance, 'Telling people about cookies'",
    ),
    ComplianceCheck(
        id="ICO-003",
        framework="ICO",
        category="Consent Mechanism",
        title="Positive action required for consent",
        description="Users must take a clear, affirmative action to give consent. Pre-ticked boxes, implied consent from browsing, or default settings do not qualify.",
        steps=[
            "Open the consent banner or preference center.",
            "Verify consent requires an explicit click (not just closing the banner or scrolling).",
            "Check that closing the banner via X does NOT constitute acceptance.",
            "If there are toggles, verify they default to OFF for non-essential cookies.",
        ],
        expected="Consent requires explicit click on an affirmative button. Closing/dismissing does not equal acceptance.",
        severity="critical",
        references="ICO Cookie Guidance, 'Getting valid consent'",
    ),
    ComplianceCheck(
        id="ICO-004",
        framework="ICO",
        category="Consent Mechanism",
        title="Granular choices available",
        description="Users should be able to accept some types of cookies but not others.",
        steps=[
            "Open the consent preference center.",
            "Verify separate toggles exist for different cookie categories.",
            "Test selecting analytics but not marketing (or vice versa).",
            "Save preferences and verify only the selected category's cookies are set.",
        ],
        expected="Per-category toggles work independently. Saving partial preferences sets only the chosen category's cookies.",
        severity="major",
        references="ICO Cookie Guidance, 'Providing granular choices'",
    ),
    ComplianceCheck(
        id="ICO-005",
        framework="ICO",
        category="Consent Refresh",
        title="Regular consent refresh",
        description="ICO recommends periodically refreshing consent rather than relying on a one-time choice indefinitely.",
        steps=[
            "Accept cookies and find the consent record cookie.",
            "Check the expiry — is it reasonable (6-12 months)?",
            "Consider: does the site ever re-prompt for consent after changes to cookie usage?",
        ],
        expected="Consent cookie has a reasonable expiry (6-12 months). Site re-prompts when cookie policy changes.",
        severity="minor",
        references="ICO Cookie Guidance, 'Refreshing consent'",
    ),
    ComplianceCheck(
        id="ICO-006",
        framework="ICO",
        category="Third Parties",
        title="Third-party cookies disclosed and consented to",
        description="If third-party cookies are used, users must be informed and must consent to each third party.",
        steps=[
            "Accept all cookies.",
            "In DevTools, identify all third-party domain cookies.",
            "Cross-reference with the cookie policy — is each third party named?",
            "Verify the consent mechanism covers third-party cookies explicitly.",
        ],
        expected="All third-party cookie providers are named in the policy. Consent covers them explicitly.",
        severity="major",
        automated=True,
        references="ICO Cookie Guidance, 'Third party cookies'",
    ),
]

# ---------------------------------------------------------------------------
# WCAG 2.2 AA — Web Content Accessibility Guidelines (consent banner focus)
# ---------------------------------------------------------------------------
WCAG_CHECKS: list[ComplianceCheck] = [
    ComplianceCheck(
        id="WCAG-001",
        framework="WCAG",
        category="Keyboard",
        title="Banner fully keyboard accessible",
        description="All interactive elements in the consent banner must be operable via keyboard alone (Tab, Shift+Tab, Enter, Space). No keyboard traps.",
        steps=[
            "Load the page and do NOT use the mouse.",
            "Press Tab repeatedly. Verify focus moves through every button in the banner (Accept, Reject, Customize, links).",
            "Press Shift+Tab to verify reverse navigation works.",
            "Press Enter or Space on each focused button and verify it activates.",
            "Confirm there is no keyboard trap — you can Tab past the banner into the page.",
        ],
        expected="Every banner button is reachable and activatable via keyboard. No element is skipped or traps focus.",
        severity="critical",
        automated=True,
        references="WCAG 2.1.1 Keyboard (Level A)",
    ),
    ComplianceCheck(
        id="WCAG-002",
        framework="WCAG",
        category="Focus",
        title="Focus moves to banner on page load",
        description="When the consent banner appears, focus should move to the banner or its first interactive element so keyboard and screen-reader users are aware of it immediately.",
        steps=[
            "Load the page in a fresh session.",
            "Without pressing any key, check which element has focus (browser DevTools or screen reader).",
            "Verify focus is on the banner, a heading inside it, or its first button.",
            "If focus is NOT on the banner, press Tab once and check if the first Tab stop is in the banner.",
        ],
        expected="Focus is on the banner or its first interactive element on page load, or the banner is the first Tab stop.",
        severity="major",
        automated=True,
        references="WCAG 2.4.3 Focus Order (Level A)",
    ),
    ComplianceCheck(
        id="WCAG-003",
        framework="WCAG",
        category="Focus",
        title="Visible focus indicator on all controls",
        description="Every interactive element in the banner must show a clearly visible focus ring or outline when focused via keyboard.",
        steps=[
            "Tab through each button and link in the consent banner.",
            "For each element, verify a visible focus indicator (outline, ring, border change) is displayed.",
            "Check that the indicator has sufficient contrast against the banner background.",
            "Verify focus is not suppressed via CSS (outline: none without replacement).",
        ],
        expected="All buttons and links show a clearly visible, high-contrast focus indicator when focused.",
        severity="major",
        references="WCAG 2.4.7 Focus Visible (Level AA)",
    ),
    ComplianceCheck(
        id="WCAG-004",
        framework="WCAG",
        category="Focus",
        title="Focus not obscured by banner",
        description="WCAG 2.2 requires that when a UI element receives focus, it is not entirely hidden by other content. The consent banner must not cover the focused element behind it.",
        steps=[
            "With the consent banner visible, Tab through elements on the main page (behind the banner).",
            "Check if any focused element is completely hidden behind the banner overlay.",
            "If the banner has a semi-transparent overlay, verify focused elements behind it are still partially visible.",
            "After dismissing the banner, confirm focus returns to the page content without any element hidden.",
        ],
        expected="No focused element is entirely hidden by the banner. Focus is visible at all times.",
        severity="major",
        references="WCAG 2.4.11 Focus Not Obscured (Minimum) (Level AA) — New in 2.2",
    ),
    ComplianceCheck(
        id="WCAG-005",
        framework="WCAG",
        category="Color & Contrast",
        title="Text meets 4.5:1 contrast ratio",
        description="All text in the consent banner must meet the WCAG AA minimum contrast ratio of 4.5:1 for normal text and 3:1 for large text (18pt+ or 14pt bold).",
        steps=[
            "Identify all text in the banner (heading, body, button labels, links).",
            "Use a contrast checker (DevTools, axe, Colour Contrast Analyser) to measure foreground vs background ratio.",
            "Verify normal text meets 4.5:1 minimum.",
            "Verify large text (18pt+ or 14pt bold) meets 3:1 minimum.",
            "Check both button text and link text.",
        ],
        expected="All text meets 4.5:1 (normal) or 3:1 (large) contrast ratio against its background.",
        severity="major",
        automated=True,
        references="WCAG 1.4.3 Contrast (Minimum) (Level AA)",
    ),
    ComplianceCheck(
        id="WCAG-006",
        framework="WCAG",
        category="Target Size",
        title="Interactive targets at least 24x24 CSS pixels",
        description="WCAG 2.2 requires that interactive targets (buttons, links, toggles) have a minimum size of 24x24 CSS pixels to be easily operable.",
        steps=[
            "Inspect each button and link in the consent banner using DevTools.",
            "Measure the clickable area (width x height in CSS pixels) of each interactive element.",
            "Verify every target is at least 24x24 CSS pixels.",
            "Pay special attention to close (X) buttons and small links which often fail this criterion.",
            "If toggles exist in the preference center, measure those too.",
        ],
        expected="All interactive elements are at least 24x24 CSS pixels. No undersized targets.",
        severity="major",
        automated=True,
        references="WCAG 2.5.8 Target Size (Minimum) (Level AA) — New in 2.2",
    ),
    ComplianceCheck(
        id="WCAG-007",
        framework="WCAG",
        category="Screen Reader",
        title="Banner has proper ARIA landmark and labels",
        description="The consent banner should use appropriate ARIA roles and labels so screen readers announce it correctly as a dialog or region.",
        steps=[
            "Inspect the banner element in DevTools.",
            "Check for: role='dialog' or role='alertdialog', aria-label or aria-labelledby, aria-describedby.",
            "If the banner is an iframe, verify it has a descriptive title attribute.",
            "Activate a screen reader (VoiceOver on Mac: Cmd+F5). Navigate to the banner and verify it is announced with its purpose.",
            "Verify buttons are announced with their action (e.g., 'Accept all cookies, button').",
        ],
        expected="Banner has role='dialog' with aria-label. Buttons have descriptive accessible names. Screen reader announces the banner's purpose.",
        severity="major",
        automated=True,
        references="WCAG 4.1.2 Name, Role, Value (Level A); ARIA Authoring Practices — Dialog",
    ),
    ComplianceCheck(
        id="WCAG-008",
        framework="WCAG",
        category="Reflow",
        title="Banner usable at 400% zoom without horizontal scroll",
        description="The consent banner must reflow to fit the viewport at 400% zoom (320 CSS pixels wide) without requiring horizontal scrolling.",
        steps=[
            "Set browser zoom to 400% (or resize viewport to 320px wide).",
            "Verify the consent banner is fully visible and readable.",
            "Check that all buttons are accessible and not cut off or overlapping.",
            "Verify no horizontal scrollbar is needed to read the banner or reach buttons.",
            "Test the preference center (if present) at 400% zoom as well.",
        ],
        expected="Banner reflows to a single column, all text readable, all buttons reachable at 400% zoom. No horizontal scroll.",
        severity="major",
        references="WCAG 1.4.10 Reflow (Level AA)",
    ),
    ComplianceCheck(
        id="WCAG-009",
        framework="WCAG",
        category="Motion",
        title="No motion or animation that cannot be disabled",
        description="If the consent banner uses animation (slide-in, fade, bounce), users must be able to disable it. Animations should respect prefers-reduced-motion.",
        steps=[
            "Load the page and observe how the banner appears.",
            "Note any animation (slide up, fade in, bounce, pulse on buttons).",
            "In OS settings, enable 'Reduce motion' (macOS: System Settings → Accessibility → Display).",
            "Reload the page and verify the banner appears without animation.",
            "Check CSS for @media (prefers-reduced-motion: reduce) rules.",
        ],
        expected="Banner respects prefers-reduced-motion. Animations are removed or replaced with instant transitions when reduced motion is enabled.",
        severity="minor",
        references="WCAG 2.3.3 Animation from Interactions (Level AAA, but best practice at AA)",
    ),
    ComplianceCheck(
        id="WCAG-010",
        framework="WCAG",
        category="Language",
        title="Banner language matches page lang attribute",
        description="The consent banner text must be in the same language as declared by the page's lang attribute, or have its own lang attribute if different.",
        steps=[
            "Check the page's <html lang='...'> attribute.",
            "Verify the consent banner text is in the declared language.",
            "If the banner is in a different language from the page, check for a lang attribute on the banner element.",
            "Verify screen reader will pronounce the text correctly based on the language declaration.",
        ],
        expected="Banner language matches the page lang attribute. If different, the banner has its own lang attribute.",
        severity="minor",
        automated=True,
        references="WCAG 3.1.1 Language of Page (Level A); 3.1.2 Language of Parts (Level AA)",
    ),
]


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------
ALL_FRAMEWORKS = {
    "GDPR": GDPR_CHECKS,
    "ePrivacy": EPRIVACY_CHECKS,
    "EDPB": EDPB_CHECKS,
    "Planet49": PLANET49_CHECKS,
    "CNIL": CNIL_CHECKS,
    "ICO": ICO_CHECKS,
    "WCAG": WCAG_CHECKS,
}

ALL_CHECKS: list[ComplianceCheck] = (
    GDPR_CHECKS + EPRIVACY_CHECKS + EDPB_CHECKS + PLANET49_CHECKS + CNIL_CHECKS + ICO_CHECKS + WCAG_CHECKS
)


def get_checks_by_framework(framework: str) -> list[ComplianceCheck]:
    """Return all checks for a specific framework."""
    return ALL_FRAMEWORKS.get(framework, [])


def get_automated_checks() -> list[ComplianceCheck]:
    """Return checks that can be partially verified by automation."""
    return [c for c in ALL_CHECKS if c.automated]


def get_manual_only_checks() -> list[ComplianceCheck]:
    """Return checks that require manual verification."""
    return [c for c in ALL_CHECKS if not c.automated]
