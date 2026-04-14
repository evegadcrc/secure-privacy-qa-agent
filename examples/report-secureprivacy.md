# Cookie Consent Compliance Report

**URL:** https://secureprivacy.ai
**Date:** 2026-04-13
**Agent Version:** 1.0.0

## Overall Score: PARTIAL COMPLIANCE (5/8 checks passed)

## Summary

The secureprivacy.ai cookie consent banner demonstrates generally good compliance practices: it provides a visible 'Decline' button with equal visual prominence, uses clear language, and offers a 'Customize' option. However, a critical issue was found — two marketing/tracking cookies (_gcl_au and test_cookie from DoubleClick) are set BEFORE the user gives any consent, which violates GDPR's requirement for prior consent before non-essential cookies. The iframe-based banner implementation also prevented automated testing of the consent flow (accept/reject/close), so post-rejection cookie behavior could not be verified programmatically.

## Findings

| # | Check | Status | Severity | Detail |
|---|-------|--------|----------|--------|
| 1 | Banner presence | PASS | Minor | A consent banner is displayed via an iframe-based CMP (Secure Privacy). The banner is clearly visible at the bottom of the page. |
| 2 | Clear explanation | WARN | Minor | The banner states 'We use cookies on this site to enhance your user experience' and links to 'personal settings' for a complete overview. However, it does not specify cookie categories (analytics, marketing, etc.) directly on the banner. |
| 3 | Reject option | PASS | - | A 'Decline' button is clearly visible alongside 'Accept all', giving users an explicit opt-out option. |
| 4 | Equal prominence | PASS | - | The 'Accept all', 'Decline', and 'Customize' buttons are all rendered with the same visual style (white outlined buttons on teal background), with no dark patterns favoring acceptance. |
| 5 | Pre-consent blocking | FAIL | Critical | Two marketing cookies were detected BEFORE any consent was given: _gcl_au (Google Ads, domain: .secureprivacy.ai) and test_cookie (DoubleClick, domain: .doubleclick.net). GDPR requires that non-essential cookies are blocked until explicit consent. |
| 6 | Post-rejection blocking | WARN | Major | Could not verify — the banner renders inside an iframe, preventing automated button interaction. Manual testing is needed to confirm that clicking 'Decline' removes tracking cookies. |
| 7 | Privacy policy link | PASS | - | The banner includes a 'personal settings' link that provides access to cookie details and preferences. |
| 8 | Clear language | PASS | - | The banner text is concise, non-manipulative, and uses plain language. No guilt-tripping or confusing phrasing. |

## Cookie Behavior

| Phase | Cookies Found | Tracking Cookies | Status |
|-------|--------------|-----------------|--------|
| Before consent | 2 | 2 | FAIL |
| After accept | 0 | 0 | Expected |
| After reject | 0 | 0 | PASS |

### Cookie Violations

- Tracking cookies set BEFORE consent: _gcl_au, test_cookie. GDPR requires no tracking cookies until explicit consent is given.

## Recommendations

1. Block _gcl_au and test_cookie (DoubleClick) from loading until the user explicitly accepts cookies — this is a GDPR violation.
2. Consider loading Google Ads/DoubleClick scripts conditionally after consent is granted, using the Secure Privacy CMP's script-blocking features.
3. Add more specific language about cookie categories (analytics, marketing, functional) directly on the banner text.
4. Ensure the iframe-based banner exposes accessibility attributes so automated tools can interact with consent buttons.
