# Cookie Consent Compliance Audit Guidelines

**Version:** 1.0
**Last Updated:** 2026-04-13
**Scope:** GDPR, ePrivacy Directive, CCPA/CPRA, LGPD, and 55+ global privacy laws

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Legal Framework Overview](#2-legal-framework-overview)
3. [Audit Criteria by Severity](#3-audit-criteria-by-severity)
4. [Dark Patterns Detection](#4-dark-patterns-detection)
5. [Cookie Categorization Standards](#5-cookie-categorization-standards)
6. [Consent Flow Testing](#6-consent-flow-testing)
7. [CMP-Specific Testing](#7-cmp-specific-testing)
8. [Accessibility Requirements](#8-accessibility-requirements)
9. [Global Privacy Law Matrix](#9-global-privacy-law-matrix)
10. [Technical Testing Methodology](#10-technical-testing-methodology)
11. [Known Limitations of Automated Testing](#11-known-limitations-of-automated-testing)
12. [Enforcement Precedents](#12-enforcement-precedents)
13. [References](#13-references)

---

## 1. Purpose

This document provides comprehensive guidelines for auditing the cookie consent compliance tests performed by the Cookie Consent QA Agent. It serves as the authoritative reference for:

- Evaluating whether a website's cookie consent implementation meets legal requirements
- Identifying gaps in our automated test coverage
- Scoring and prioritizing findings by severity
- Understanding which regulations apply based on user jurisdiction

The QA agent audits websites against 8 core criteria. These guidelines expand on the legal basis, testing methodology, and expected outcomes for each.

---

## 2. Legal Framework Overview

### 2.1 EU: GDPR + ePrivacy Directive (Opt-In Model)

The EU framework is the strictest and requires **prior opt-in consent** before any non-essential cookies are placed.

**GDPR (Regulation 2016/679)**
- **Article 4(11)** defines consent as: *freely given, specific, informed, and unambiguous indication* by a *clear affirmative action*.
- **Article 6(1)(a)** establishes consent as a legal basis for processing.
- **Article 7** sets conditions: controller must demonstrate consent was given; withdrawal must be as easy as giving consent; consent must be distinguishable from other matters.
- **Recital 32** explicitly states: *"Silence, pre-ticked boxes or inactivity should not constitute consent."*

**ePrivacy Directive (2002/58/EC, Article 5(3))**
- Governs the *act of storing/accessing information* on a user's device (the cookie itself).
- Is *lex specialis* to GDPR -- it applies specifically to cookies/device access, while GDPR covers the subsequent data processing.
- Consent standard is defined by reference to GDPR Article 4(11).
- **Only exemption:** cookies that are *strictly necessary* to provide a service explicitly requested by the user (session cookies, auth tokens, load balancing, consent preference cookies).
- There is **no "legitimate interest" basis** for placing non-essential cookies under ePrivacy. Consent is the *only* legal basis.

**Key CJEU ruling -- Planet49 (C-673/17, October 2019):**
- Pre-ticked checkboxes do NOT constitute valid consent.
- Applies regardless of whether cookies involve personal data.
- Information must include cookie duration and third-party access details.

**EDPB Guidelines 05/2020 on Consent:**
- Scrolling or continued browsing is NOT valid consent.
- Cookie walls are presumptively invalid (consent is not freely given).
- Bundled "all or nothing" consent is invalid -- granularity is required.
- Consent must be granular per purpose.

### 2.2 US: CCPA/CPRA (Opt-Out Model)

The US framework is fundamentally different: tracking is allowed by default, but users must have the right to opt out.

**CCPA (Cal. Civ. Code 1798.100+)**
- Businesses may collect personal information (including via cookies) by default.
- Must provide a **"Do Not Sell or Share My Personal Information"** link on the homepage.
- Opt-out must be effectuated within 15 business days.
- Must not require account creation to opt out.

**CPRA Amendments (Proposition 24, effective 2023):**
- Added **"sharing"** as a regulated activity (covers cross-context behavioral advertising via cookies/pixels even without money changing hands).
- Added **"Limit the Use of My Sensitive Personal Information"** link requirement.
- Businesses may combine both links into **"Your Privacy Choices"**.
- **Dark patterns defined** in statute (Section 1798.140(l)): any consent obtained through dark patterns is void.
- Created the **CPPA** (California Privacy Protection Agency) as a dedicated enforcer.

**Global Privacy Control (GPC):**
- Browser-level signal via `Sec-GPC: 1` HTTP header and `navigator.globalPrivacyControl` JS API.
- **Legally binding under:** CCPA/CPRA (California), CPA (Colorado, from July 2024), CTDPA (Connecticut, from Jan 2025), TDPSA (Texas, from Jan 2025), Oregon, Montana.
- **Not legally binding under:** Virginia (VCDPA), Utah (UCPA).
- Per the *Sephora* enforcement ($1.2M fine, Aug 2022), failure to honor GPC is a CCPA violation.

### 2.3 Brazil: LGPD

**LGPD (Lei Geral de Proteção de Dados, Law 13,709/2018):**
- Requires "free, informed, and unambiguous" consent for processing personal data.
- **No ePrivacy equivalent** -- Brazil does not have a cookie-specific directive. Cookie regulation falls under general data processing rules.
- **Legitimate interest is broader** than in GDPR -- the ANPD (Brazilian DPA) has been more permissive about analytics cookies under legitimate interest.
- Best practice is to display a consent banner with opt-out capability for analytics/marketing cookies, even if strict prior opt-in is not legally mandated for all cookies.
- Consent must be granular per purpose (Article 8, para 4).
- Revocation must be as easy as giving consent (Article 8, para 5).

### 2.4 IAB Transparency & Consent Framework (TCF) 2.2

TCF is an industry self-regulatory framework, not law, but is the de facto standard for programmatic advertising compliance in the EU.

**Key requirements:**
- Defines 11 purposes for data processing. Purpose 1 ("Store and/or access information on a device") always requires explicit consent -- no legitimate interest basis allowed.
- **TC String** (`euconsent-v2` cookie) encodes the user's consent choices.
- **CMP API** (`__tcfapi`) must be available on the page before ad scripts load.
- Must show names and count of vendors seeking consent.
- All consent must go through the CMP (no "out-of-band" consent).

---

## 3. Audit Criteria by Severity

### CRITICAL -- Must fix immediately (legal violations)

| # | Criterion | Legal Basis | What to Check |
|---|-----------|-------------|---------------|
| C1 | **No tracking cookies before consent** | ePrivacy Art 5(3), GDPR | Load page with clean profile. Before ANY banner interaction, capture all cookies. Any analytics/marketing cookies = CRITICAL FAIL. Also check network requests to known tracking domains (google-analytics.com, doubleclick.net, facebook.com/tr, etc.) |
| C2 | **Reject option exists at first layer** | EDPB 05/2020, CNIL enforcement (Google 150M EUR, Facebook 60M EUR fines) | Banner must have a "Reject All" / "Decline" / "Refuse" button at the SAME layer/screen as "Accept All." Having only "Accept All" and "Manage Preferences" is non-compliant. |
| C3 | **Pre-ticked boxes absent** | Planet49 (C-673/17), EDPB 05/2020, Recital 32 | In the preference/settings panel, NO non-essential cookie category may be pre-selected/pre-toggled. Consent requires affirmative opt-in action. |
| C4 | **Tracking cookies removed after rejection** | ePrivacy Art 5(3) | After clicking "Reject All," capture cookies. Any analytics/marketing cookies remaining = CRITICAL FAIL. Also verify no tracking network requests fire after rejection. |
| C5 | **Third-party scripts blocked before consent** | ePrivacy Art 5(3) | Monitor network requests on page load. Scripts from tracking domains (Google Analytics, Facebook, DoubleClick, etc.) must NOT execute before consent. |

### MAJOR -- Significant compliance risk

| # | Criterion | Legal Basis | What to Check |
|---|-----------|-------------|---------------|
| M1 | **Equal visual prominence** | EDPB 03/2022, CNIL enforcement | Accept and Reject buttons must have similar size, color contrast, position, and element type (both buttons, not button vs. link). Compare CSS: font-size, padding, background-color, border, dimensions. |
| M2 | **Click parity** | EDPB 03/2022, CNIL enforcement | Count clicks to accept all vs. clicks to reject all. Must be equal (ideally 1 each). If rejecting requires 2+ more clicks than accepting = MAJOR violation (dark pattern). |
| M3 | **Consent withdrawal mechanism** | GDPR Art 7(3) | After banner dismissal, there must be a persistent, easily accessible way to re-open preferences (floating icon, footer link labeled "Cookie Settings," etc.). |
| M4 | **Withdrawal as easy as giving consent** | GDPR Art 7(3) | Compare clicks to give consent vs. clicks to withdraw. Must be comparable. |
| M5 | **Consent record stored** | GDPR Art 7(1) | A consent cookie must record: timestamp, specific choices, version of consent text. Check for common consent cookies (CookieConsent, OptanonConsent, euconsent-v2, sp_consent, etc.). |
| M6 | **Granular category consent** | GDPR Art 4(11) "specific" | Preference center must offer independent toggles per category (Necessary, Analytics, Marketing, Functional). Must NOT be "all or nothing." |
| M7 | **Clear, non-manipulative language** | EDPB 03/2022, GDPR Art 7(2) | Banner text must be neutral and informational. No confirmshaming, emotional steering, guilt-tripping, or urgency language. No double negatives or confusing toggles. |
| M8 | **GPC signal honored** (US sites) | CCPA/CPRA, CPA, CTDPA, TDPSA | Send requests with `Sec-GPC: 1` and verify: no marketing cookies set, no third-party ad requests made. CMP should treat GPC as valid opt-out of sale/sharing. |
| M9 | **"Do Not Sell or Share" link present** (US sites) | CCPA/CPRA | Homepage must contain a "Do Not Sell or Share My Personal Information" link (or combined "Your Privacy Choices") leading to a working opt-out mechanism. |
| M10 | **Post-rejection script blocking** | ePrivacy Art 5(3) | After rejection, tracking scripts must not execute. Monitor for script reloads, delayed tag firings, or race conditions. |

### MINOR -- Best practice / compliance improvement

| # | Criterion | Legal Basis | What to Check |
|---|-----------|-------------|---------------|
| m1 | **Privacy/cookie policy link in banner** | Planet49, ePrivacy Art 5(3) | Banner must contain a link to the full cookie/privacy policy. |
| m2 | **Cookie purpose explanation** | GDPR "informed" consent | Banner should explain what cookies are used for, ideally listing categories. |
| m3 | **Cookie lifetime disclosure** | Planet49 | Cookie policy must include duration of each cookie and whether third parties access it. |
| m4 | **Secure cookie attributes** | Security best practice | Cookies over HTTPS should have `Secure` flag. Session cookies should have `HttpOnly`. `SameSite` should be set (Lax or Strict for first-party). |
| m5 | **Reasonable cookie lifetimes** | CNIL guidance | Consent cookie: max 6-13 months. Tracking cookies should not exceed stated purposes. |
| m6 | **Consent persists across sessions** | GDPR, CCPA | On return visit, banner should NOT reappear if consent was previously given/rejected. Choice must be remembered. |
| m7 | **TCF API present and functional** (if serving EU ads) | TCF 2.2 | `__tcfapi` available, TC string parseable, consent state matches user choices. |
| m8 | **Banner responsive design** | Best practice | Banner must work correctly on mobile viewports (320px+). |

---

## 4. Dark Patterns Detection

### 4.1 EDPB Dark Pattern Taxonomy (Guidelines 03/2022)

| Category | Pattern | Description | Detection Method |
|----------|---------|-------------|-----------------|
| **Overloading** | Continuous prompting | Repeatedly asking after decline | Monitor for banner reappearance after rejection |
| **Overloading** | Privacy maze | Many clicks to reject | Count interaction steps for rejection path |
| **Skipping** | Deceptive snugness | Pre-ticked non-essential categories | Check initial state of toggles/checkboxes in preference panel |
| **Stirring** | Emotional steering | Guilt-tripping language ("You'll miss out...") | NLP/LLM analysis of banner text |
| **Stirring** | Hidden in plain sight | Reject as text link, accept as button | Compare element types and CSS styling |
| **Hindering** | Dead end | Reject leads to error or loops | Test reject path and verify completion |
| **Hindering** | Longer than necessary | Accept = 1 click, reject = 3+ clicks | Count and compare click paths |
| **Hindering** | Misleading info | "Site won't work without cookies" | LLM analysis of banner text |
| **Fickle** | Lacking hierarchy | Confusing category presentation | Structural analysis of preference panel |
| **Fickle** | Ambiguous wording | Double negatives, confusing toggles | NLP/LLM analysis of label text |
| **Left in dark** | Conflicting info | Banner contradicts cookie policy | Cross-reference banner text with policy |
| **Left in dark** | Language discontinuity | Banner in different language than site | Compare language of banner vs. page |

### 4.2 Specific Automated Checks

**Button asymmetry detection:**
```
For accept_button and reject_button:
  Compare: font-size, padding, width, height
  Compare: background-color contrast ratio
  Compare: element type (button vs. a/span)
  Compare: border presence and styling
  Compare: position (above-fold vs. below-fold)
  FAIL if reject significantly less prominent
```

**Click count comparison:**
```
accept_clicks = count steps from banner appearance to consent given
reject_clicks = count steps from banner appearance to consent rejected
FAIL if reject_clicks > accept_clicks + 1
```

**Pre-checked toggle detection:**
```
In preference/settings panel:
  For each category toggle/checkbox:
    If category != "strictly necessary":
      FAIL if toggle.checked == true (default state)
```

### 4.3 CNIL-Specific Requirements (France)

CNIL has the strictest enforcement on dark patterns. Their specific mandates:

- **Symmetric choices**: Refusing must be as easy as accepting. A "Refuse All" button must exist at the same level as "Accept All."
- **No cookie walls**: Conditioning site access on acceptance is generally invalid consent.
- **Continued browsing is NOT consent**: Scrolling or navigating away from the banner is not an affirmative action.
- **Banner must persist**: The banner must not auto-dismiss before the user makes an active choice.
- **Cookie lifetime limits**: Consent cookies max 13 months; re-prompt after max 6 months.

---

## 5. Cookie Categorization Standards

### 5.1 Standard Categories

| Category | Consent Required | Default State | Examples | Handling Rule |
|----------|-----------------|---------------|----------|---------------|
| **Strictly Necessary** | No (ePrivacy exemption) | Active (non-toggleable) | Session ID, CSRF token, auth cookie, consent preference, load balancer | Always allowed. Must genuinely be necessary -- cannot include analytics or marketing. |
| **Functional / Preferences** | Yes | Inactive (opt-in) | Language selection, UI theme, accessibility settings, recently viewed | Block until consent. Some DPAs accept legitimate interest for basic functionality. |
| **Analytics / Statistics** | Yes* | Inactive (opt-in) | `_ga`, `_gid`, Matomo, Hotjar, Adobe Analytics | Block until consent. *Exception: some DPAs (CNIL, Dutch) allow privacy-friendly first-party analytics without consent (anonymized IP, no cross-site, no third-party sharing). Does NOT apply to standard Google Analytics. |
| **Marketing / Advertising** | Yes (always) | Inactive (opt-in) | `_gcl_au`, `_fbp`, `IDE`, DoubleClick, retargeting pixels | Strictest category. Always requires explicit consent. No legitimate interest basis. Involves third-party data sharing. |
| **Social Media** | Yes | Inactive (opt-in) | Facebook Connect, Twitter widgets, LinkedIn Insight, YouTube embeds | Block until consent. Typically third-party cookies enabling cross-site tracking. |

### 5.2 Known Tracking Cookie Patterns (for automated classification)

**Analytics cookies (consent required):**
`_ga`, `_gid`, `_gat`, `__utma`, `__utmb`, `__utmc`, `__utmz`, `_clck`, `_clsk`

**Marketing cookies (consent required):**
`_gcl_au`, `_gcl_aw`, `_fbp`, `_fbc`, `fr`, `IDE`, `DSID`, `test_cookie`, `_tt_`, `_ttp`, `_pin_unauth`, `NID`, `_uetsid`, `_uetvid`, `li_sugr`, `bcookie`, `lidc`, `sc_at`, `_rdt_uuid`, `hubspotutk`, `__hssc`, `__hssrc`, `__hstc`

**Necessary cookies (no consent needed):**
`session*`, `csrf*`, `xsrf*`, `token*`, `__cfduid`, `cf_clearance`, `PHPSESSID`, `JSESSIONID`, `ASP.NET_SessionId`, `*consent*`, `OptanonConsent`, `CookieConsent`, `euconsent*`

### 5.3 Classification Rules for Auditing

1. A cookie matching a tracking pattern found BEFORE consent = **CRITICAL violation**
2. A cookie matching a tracking pattern found AFTER rejection = **CRITICAL violation**
3. A cookie classified as "unknown" should be flagged for **manual review** -- it may be miscategorized by the CMP
4. A "strictly necessary" cookie that appears to be analytics/marketing = **MAJOR violation** (over-classification abuse)
5. CMP's declared cookie inventory should be compared against actual cookies found -- undeclared cookies are a compliance gap

---

## 6. Consent Flow Testing

### 6.1 Test Matrix

Each flow must be tested independently, starting from a clean browser state (cleared cookies, storage, and cache).

| Flow | Steps | Expected Banner Behavior | Expected Cookie Behavior |
|------|-------|--------------------------|--------------------------|
| **Fresh visit** | Navigate to page, do nothing | Banner appears, visible, no auto-dismiss | Only strictly necessary cookies present |
| **Accept All** | Navigate > Click "Accept All" | Banner dismisses | All declared cookies may be set. Consent cookie recorded. |
| **Reject All** | Navigate > Click "Reject/Decline" | Banner dismisses | No tracking/analytics/marketing cookies. Only necessary + consent cookie. |
| **Customize > Accept Some** | Navigate > Click "Manage" > Toggle analytics ON, marketing OFF > Save | Banner dismisses | Only analytics cookies set. No marketing cookies. Consent cookie reflects granular choice. |
| **Customize > Reject All** | Navigate > Click "Manage" > Leave all OFF > Save | Banner dismisses | No tracking cookies. Consent cookie recorded. |
| **Close/Dismiss** | Navigate > Click X or close | Banner dismisses | No tracking cookies (closing without affirmative consent = no consent given). |
| **Return visit (accepted)** | Navigate (with prior accept consent cookie) | Banner does NOT reappear | Previously consented cookies may be present |
| **Return visit (rejected)** | Navigate (with prior reject consent cookie) | Banner does NOT reappear | No tracking cookies |
| **Consent withdrawal** | After accept > find settings link > change to reject > save | Preference panel opens with current state | Tracking cookies removed after withdrawal |
| **GPC enabled** | Navigate with `Sec-GPC: 1` header | Banner may show (varies) | No marketing/advertising cookies. Sale/sharing opted out. |

### 6.2 Post-Consent Verification Checklist

After each flow action, verify:

- [ ] Banner dismissed (or persisted, as appropriate)
- [ ] Cookie count matches expectations for the flow
- [ ] No tracking cookies in unexpected states
- [ ] Consent cookie is set with correct values
- [ ] Network requests to tracking domains match consent state
- [ ] `localStorage` and `sessionStorage` do not contain tracking data
- [ ] If TCF: `euconsent-v2` cookie and `__tcfapi` reflect the correct consent state

---

## 7. CMP-Specific Testing

### 7.1 Secure Privacy (secureprivacy.ai)

**Architecture:** Secure Privacy uses an **iframe-based** banner with `id="ifrmCookieBanner"`. The iframe uses `srcdoc` and content is injected asynchronously by their JavaScript.

**Known characteristics:**
- Banner renders inside `<iframe id="ifrmCookieBanner" role="application" aria-label="Cookie Banner">`
- Content is populated asynchronously (initial `srcdoc` has empty `<body>`)
- Buttons (Accept all, Decline, Customize) render inside the iframe
- Geo-targeted: different banner for EU vs. US vs. other regions
- Claims TCF 2.2 support (verify CMP ID on IAB's CMP list)
- Claims Google Consent Mode v2 integration
- Claims GPC signal detection

**Testing challenges:**
- Standard DOM selectors from parent page cannot reach elements inside the iframe
- Playwright requires `page.frame_locator('#ifrmCookieBanner')` or `page.frames` to interact
- Content loads asynchronously -- must wait for elements inside the iframe to be visible
- Cross-origin restrictions may apply depending on how content is loaded

**Recommended Playwright approach:**
```python
# Detect iframe-based banner
frame = page.frame_locator('#ifrmCookieBanner')
# Wait for content to load
await frame.locator('button').first.wait_for(state='visible', timeout=10000)
# Extract text
text = await frame.locator('body').inner_text()
# Click buttons
await frame.locator('button:has-text("Decline")').click()
```

**Known iframe CMP IDs to detect:**
- `#ifrmCookieBanner` -- Secure Privacy
- `#CybotCookiebotDialog` -- Cookiebot (usually not iframe, but may use one)
- `.sp-message-container iframe` -- SourcePoint
- `#truste-consent-track iframe` -- TrustArc

### 7.2 Common CMP Failure Modes

These are the most frequent compliance failures found across CMPs (based on academic research by Santos et al. 2021, Nouwens et al. 2020, Matte et al. 2020):

| # | Failure Mode | Description | How to Detect |
|---|-------------|-------------|---------------|
| 1 | **Race condition** | Tracking scripts fire before CMP blocks them | Check cookies immediately on page load (before banner interaction) |
| 2 | **Tag manager bypass** | Scripts in GTM/other tag managers evade CMP blocking | Monitor network requests for tracking domains pre-consent |
| 3 | **Script chain leakage** | Blocked script already loaded a child script that sets cookies | Full network request audit pre-consent |
| 4 | **Iframe cookie leakage** | Third-party iframes (ads, embeds) set cookies independently | Capture ALL cookies including third-party domains |
| 5 | **Server-side cookies** | `Set-Cookie` headers bypass client-side CMP | Check response headers for tracking cookies |
| 6 | **Consent desynchronization** | Consent cookie expires but tracking cookies remain | Test with expired consent state |
| 7 | **CDN/cache issues** | Cached pages include tracking scripts despite CMP | Test with cache-busting headers |
| 8 | **Consent string corruption** | TCF TC string becomes malformed | Parse and validate `euconsent-v2` cookie |
| 9 | **Undeclared cookies** | Actual cookies exceed CMP's declared inventory | Compare CMP declarations vs. actual cookies |
| 10 | **Missing prior blocking** | CMP records consent choice but doesn't actually block scripts | Verify by checking script execution, not just consent state |

---

## 8. Accessibility Requirements

Cookie consent banners are web content and must meet WCAG 2.1/2.2 Level AA standards. The European Accessibility Act (EAA, effective June 2025) makes this a legal requirement via EN 301 549.

### 8.1 Keyboard Navigation (WCAG 2.1.1, 2.1.2)

- [ ] All buttons, toggles, and links operable via keyboard (Tab, Enter, Space)
- [ ] No keyboard traps -- user can tab through and past the banner
- [ ] Logical tab order (info text > manage/reject/accept)
- [ ] If modal: focus trapped within banner, Escape key closes it
- [ ] Enter/Space activates buttons; Space toggles checkboxes

### 8.2 Screen Reader Compatibility (WCAG 4.1.2, 1.3.1)

- [ ] Banner uses `role="dialog"` or `role="alertdialog"` with `aria-label` or `aria-labelledby`
- [ ] `aria-modal="true"` if the banner blocks page interaction
- [ ] All buttons have accessible names (visible text or `aria-label`)
- [ ] Toggle states use `aria-checked`, `aria-pressed`, or native checkbox
- [ ] Category descriptions associated with toggles via `aria-describedby` or `<label>`
- [ ] Status changes announced via `aria-live` regions
- [ ] Banner announced when it appears

### 8.3 Color Contrast (WCAG 1.4.3, 1.4.11)

- [ ] Text: minimum 4.5:1 ratio (normal text) or 3:1 (large text: 18pt+ or 14pt+ bold)
- [ ] Interactive UI components: minimum 3:1 contrast against adjacent colors
- [ ] Color not used as sole means of conveying information (WCAG 1.4.1)

### 8.4 Focus Management (WCAG 2.4.3, 2.4.7)

- [ ] Visible focus indicator on all interactive elements (min 2px outline, 3:1 contrast)
- [ ] Focus moves to banner when it appears
- [ ] Focus returns to main content when banner dismisses
- [ ] Focused elements not obscured by the banner (WCAG 2.4.11)

### 8.5 Text and Layout (WCAG 1.4.4, 1.4.10, 1.4.12)

- [ ] Text resizable to 200% without loss of content or function
- [ ] Content reflows at 320px width without horizontal scrolling
- [ ] Text spacing adjustments (line-height 1.5x, letter-spacing 0.12em) don't break layout
- [ ] Recommended: minimum 16px base font size

---

## 9. Global Privacy Law Matrix

### Cookie/Consent Requirements by Jurisdiction

| Jurisdiction | Law | Model | Cookie Banner | Prior Blocking | Reject Button | GPC Required | Sensitive Data Link |
|-------------|-----|-------|---------------|----------------|---------------|-------------|-------------------|
| EU (27 states) | GDPR + ePrivacy | Opt-in | Required | Required | Required (first layer) | No (but recommended) | N/A |
| UK | UK GDPR + PECR | Opt-in | Required | Required | Required | No | N/A |
| California | CCPA/CPRA | Opt-out | Not required (opt-out link required) | Not required | Not required (opt-out link instead) | Yes (mandatory) | Yes ("Limit Use" link) |
| Colorado | CPA | Opt-out | Not required | Not required | Not required | Yes (from July 2024) | N/A |
| Connecticut | CTDPA | Opt-out | Not required | Not required | Not required | Yes (from Jan 2025) | N/A |
| Virginia | VCDPA | Opt-out | Not required | Not required | Not required | No | N/A |
| Texas | TDPSA | Opt-out | Not required | Not required | Not required | Yes (from Jan 2025) | N/A |
| Oregon | OCPA | Opt-out | Not required | Not required | Not required | Yes | N/A |
| Utah | UCPA | Opt-out | Not required | Not required | Not required | No | N/A |
| Brazil | LGPD | Hybrid (consent/LI) | Recommended | Not strictly required | Recommended | No | N/A |
| South Africa | POPIA | Consent | Recommended | Recommended | Recommended | No | N/A |
| Thailand | PDPA | Opt-in (GDPR-like) | Required | Required | Required | No | N/A |
| China | PIPL | Consent | Required | Required | Separate consent for cross-border | No | N/A |
| Japan | APPI | Notice-based | Recommended | Not required | Not required | No | N/A |
| Canada | PIPEDA | Meaningful consent | Recommended | Not strictly required | Recommended | No | N/A |
| Canada (Quebec) | Law 25 | Opt-in (GDPR-like) | Required | Required | Required | No | N/A |
| Australia | Privacy Act 1988 | Notice-based | Not required | Not required | Not required | No | N/A |
| India | DPDPA | Opt-in (GDPR-like) | Required | Required | Required | No | N/A |
| Switzerland | nDSG | Hybrid | Recommended | Recommended | Recommended | No | N/A |

### Geo-Targeting Implications

A CMP claiming "55+ laws" support must serve different banner configurations based on visitor jurisdiction:

- **EU/UK/Thailand/India visitors**: Full opt-in banner with prior blocking, reject button at first layer, granular categories
- **California visitors**: Opt-out notice, "Do Not Sell or Share" link, GPC honored
- **Colorado/Connecticut/Texas/Oregon visitors**: Opt-out mechanism, GPC honored
- **Brazil visitors**: Consent banner recommended, legitimate interest acceptable for some analytics
- **Unregulated jurisdictions**: May show no banner or simplified notice

---

## 10. Technical Testing Methodology

### 10.1 Testing Architecture (5 Layers)

```
Layer 1: Static Analysis (DOM/CSS)
  - Parse banner HTML structure
  - Check ARIA attributes, roles, labels
  - Evaluate color contrast, button sizing
  - Detect pre-checked toggles
  - Check for reject button presence at first layer

Layer 2: Dynamic Interaction Testing (Playwright)
  - Simulate fresh visit (clear all cookies/storage)
  - Detect and interact with consent banner
  - Test all consent paths (accept, reject, customize, close)
  - Compare cookies before/after each action
  - Test consent withdrawal flow
  - Measure click counts per path

Layer 3: Cookie & Network Audit
  - Inventory all cookies (name, domain, path, expiry, secure, httpOnly, sameSite)
  - Compare against CMP declarations
  - Categorize using known cookie databases
  - Flag undeclared cookies
  - Monitor network requests to tracking domains
  - Check localStorage/sessionStorage

Layer 4: Accessibility Audit
  - WCAG compliance of banner HTML (axe-core)
  - Keyboard navigation testing
  - Screen reader attribute verification
  - Focus management verification
  - Responsive/zoom testing

Layer 5: AI-Powered Analysis (Claude API)
  - NLP analysis of banner text for clarity/dark patterns
  - Visual analysis of banner design for asymmetries
  - Compliance scoring against regulatory checklists
  - Report generation with specific findings and remediation
```

### 10.2 Pre-Consent Cookie Capture Protocol

This is the **most critical test**. The exact sequence matters:

1. Launch browser with **clean profile** (no cookies, no storage, no cache)
2. Set user-agent to a standard browser string
3. Navigate to target URL with `wait_until="domcontentloaded"`
4. Wait 2-3 seconds for delayed scripts/CMPs to load
5. **Before ANY banner interaction**, capture:
   - All browser cookies (`context.cookies()`)
   - All localStorage entries
   - All sessionStorage entries
   - Network requests log (check for tracking domain calls)
6. Classify every captured cookie using the categorization patterns
7. Any non-necessary cookie = **CRITICAL violation**

### 10.3 Post-Consent Cookie Capture Protocol

After each consent action (accept/reject/customize):

1. Perform the consent action (click button)
2. Wait 2-3 seconds for scripts to execute and cookies to settle
3. Capture all cookies, storage, and network requests
4. Compare against pre-consent state
5. Validate:
   - **After accept**: tracking cookies may appear, consent cookie is set
   - **After reject**: NO tracking cookies, consent cookie IS set (consent cookie is "necessary")
   - **After partial consent**: only cookies matching consented categories appear

### 10.4 GPC Testing Protocol

1. Create browser context with GPC signals:
   ```python
   context = await browser.new_context(
       extra_http_headers={"Sec-GPC": "1"}
   )
   await page.add_init_script("""
       Object.defineProperty(navigator, 'globalPrivacyControl', {
           get: () => true
       });
   """)
   ```
2. Navigate to target URL
3. Verify: no marketing/advertising cookies set, no ad network requests
4. Compare behavior with GPC off vs. on

### 10.5 Iframe Detection and Interaction

For CMP implementations using iframes (like Secure Privacy):

1. After standard banner detection fails to find buttons:
2. Check for known iframe selectors: `#ifrmCookieBanner`, `[id*="cookie"] iframe`, `[id*="consent"] iframe`
3. Use `page.frame_locator()` to access iframe content
4. Wait for async content to populate inside iframe
5. Extract text and buttons from within the iframe context
6. Perform click actions through the frame locator

---

## 11. Known Limitations of Automated Testing

### What CAN be automated reliably

- Cookie inventory (before/after consent)
- Prior blocking verification
- Consent flow click-through
- Banner presence detection
- Accessibility checks (ARIA, contrast, keyboard)
- Button presence and basic styling comparison
- Pre-ticked checkbox detection
- Click count comparison
- Consent persistence across sessions
- GPC signal testing
- TCF API presence and TC string validation

### What CANNOT be fully automated

| Area | Why | Recommended Approach |
|------|-----|---------------------|
| Legal accuracy of cookie descriptions | Requires legal judgment | Flag for manual review |
| "Strictly necessary" legitimacy | Whether a cookie truly qualifies is a legal question | Flag unknown/suspicious cookies |
| Language clarity assessment | Nuance in legal sufficiency | LLM analysis + manual review |
| Emotional manipulation detection | Confirmshaming requires contextual understanding | LLM analysis + manual review |
| Privacy policy consistency | Cross-referencing full policy with banner claims | LLM-assisted comparison |
| Cross-jurisdictional applicability | Which laws apply requires legal analysis | Geo-detection + configurable rulesets |
| Third-party data sharing chains | Full chain of data recipients from cookies | Network analysis + manual investigation |
| Contextual appropriateness | Whether consent is appropriate for specific audience | Manual assessment |

---

## 12. Enforcement Precedents

### Landmark Cases (most relevant to automated testing)

| Case | Year | Fine | Key Finding | Testing Implication |
|------|------|------|-------------|-------------------|
| **CNIL v. Google** | 2021 | 150M EUR | No equally easy reject mechanism | Test for reject button at first layer (C2) |
| **CNIL v. Facebook** | 2021 | 60M EUR | Same as Google | Test for reject button at first layer (C2) |
| **CNIL v. Microsoft** | 2022 | 60M EUR | Cookies set without consent on Bing | Test pre-consent blocking (C1) |
| **CNIL v. Criteo** | 2023 | 40M EUR | Could not demonstrate valid consent | Test consent record storage (M5) |
| **CNIL v. TikTok** | 2022 | 5M EUR | No equally easy reject + insufficient info | Test reject button + explanation clarity (C2, m2) |
| **CA AG v. Sephora** | 2022 | $1.2M | Failed to honor GPC signals | Test GPC signal handling (M8) |
| **FTC v. BetterHelp** | 2023 | $7.8M | Tracking pixels sharing health data without consent | Test for tracking cookies on sensitive sites |
| **Planet49 (CJEU)** | 2019 | N/A (ruling) | Pre-ticked boxes invalid for consent | Test for pre-ticked categories (C3) |
| **FTC v. Fortnite/Epic** | 2022 | $520M | Dark patterns in consent UIs | Test for dark patterns (M1, M2, M7) |
| **Belgian DPA v. IAB Europe** | 2022 | N/A (ruling) | TC String is personal data; IAB Europe is controller | TCF implementation must be valid (m7) |

### Enforcement Trends

1. **Pre-consent cookie leakage** is the most commonly penalized violation
2. **Asymmetric reject/accept UI** is actively enforced (especially by CNIL)
3. **GPC non-compliance** is the primary US enforcement vector
4. **Dark patterns** are increasingly codified in law (CPRA) and enforced
5. **Consent proof** requirements are tightening -- "we have a CMP" is not sufficient

---

## 13. References

### EU Legal Sources
- **GDPR (Regulation 2016/679)**: Articles 4(11), 6(1)(a), 7; Recitals 32, 42, 43
- **ePrivacy Directive (2002/58/EC)**: Article 5(3), as amended by Directive 2009/136/EC
- **EDPB Guidelines 05/2020**: Consent under Regulation 2016/679
- **EDPB Guidelines 03/2022**: Deceptive design patterns in social media
- **Article 29 Working Party Opinion 04/2012**: Cookie consent exemption (WP 194)
- **Planet49 (CJEU C-673/17)**: Pre-ticked checkboxes ruling

### National DPA Guidance
- **CNIL (France)**: Guidelines on cookies and trackers (Deliberation 2020-091)
- **ICO (UK)**: Guide to PECR -- cookies and similar technologies
- **BfDI / DSK (Germany)**: TTDSG Section 25 guidance
- **Garante (Italy)**: Cookie guidelines and cookie wall enforcement

### US Legal Sources
- **CCPA**: Cal. Civ. Code 1798.100-1798.199.100
- **CPRA**: Proposition 24; CPRA Regulations (Title 11, Div. 6, Cal. Code of Regulations)
- **COPPA**: 15 U.S.C. 6501-6506; FTC COPPA Rule (16 CFR Part 312)
- **State privacy laws**: CPA (C.R.S. 6-1-1301+), VCDPA (Va. Code 59.1-575+), CTDPA, UCPA, TDPSA, OCPA

### Global Legal Sources
- **LGPD (Brazil)**: Law 13,709/2018
- **POPIA (South Africa)**: Act 4 of 2013
- **PDPA (Thailand)**: B.E. 2562
- **PIPL (China)**: Effective November 2021
- **APPI (Japan)**: Amended 2022
- **DPDPA (India)**: Act 2023

### Industry Standards
- **IAB TCF 2.2**: Policies and technical specification
- **Global Privacy Control (GPC)**: Technical specification
- **Google Consent Mode v2**: Technical documentation
- **WCAG 2.1/2.2**: Web Content Accessibility Guidelines
- **EN 301 549**: European harmonized standard for ICT accessibility

### Academic Research
- Santos et al. (2021): "Cookie Banners, What's the Purpose?"
- Nouwens et al. (2020): "Dark Patterns after the GDPR"
- Matte et al. (2020): IAB TCF compliance study
- FTC Report (2022): "Bringing Dark Patterns to Light"
