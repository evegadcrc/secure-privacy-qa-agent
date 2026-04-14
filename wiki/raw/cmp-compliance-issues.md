---
title: CMP Compliance Issues — Common Failure Modes
type: source
tags: [cmp, compliance, cookies, testing, onetrust, cookiebot, trustarc]
date_added: 2026-04-13
authority: Academic research (Santos et al., Nouwens et al., Matte et al.), DPA enforcement
---

# CMP Compliance Issues — Common Failure Modes

Based on published academic audits and DPA enforcement actions, these are the most common compliance failures across Consent Management Platforms.

## Academic Research Findings

### Santos et al. (2021) — "Cookie Banners, What's the Purpose?"
### Nouwens et al. (2020) — "Dark Patterns after the GDPR"
### Matte et al. (2020) — IAB TCF Compliance Study

Key findings across these studies:
1. **Up to 65% of websites** set tracking cookies regardless of user choice (before consent or despite rejection)
2. **~50% of EU sites** (in 2020) lacked a first-layer reject option
3. **~30% of sites** using CMPs had non-essential cookies pre-checked
4. **TCF consent string manipulation:** Some CMPs recorded consent in TC string even when users had not actively consented
5. **30-50% of actual cookies undeclared** in CMP inventories on average
6. Many CMP implementations don't actually block scripts before consent — they only record the choice
7. Many sites make consent withdrawal very difficult
8. Consent choices frequently not persisted correctly across sessions

## CMP-Specific Issues

### OneTrust
**Positive:** Market leader, comprehensive features, IAB TCF 2.2 support
**Common issues:**
- Default templates ship with "Accept" prominently styled, "Manage Preferences" as subdued link — requires manual config to add "Reject All"
- Cookie scanning sometimes miscategorizes cookies (analytics as "strictly necessary")
- Implementation can result in cookies set before consent recorded (race condition with tag managers)
- Keyboard focus management issues if not configured properly
- Preference center complex for users with hard-to-understand descriptions
- Performance impact: scripts add 200-500ms to page load

### Cookiebot (now Usercentrics)
**Positive:** Strong auto-scanning, good categorization, supports prior blocking
**Common issues:**
- Auto-categorization sometimes incorrect — human review needed
- "Decline" button historically hidden behind "Customize" in default templates (improved recently)
- Third-party scripts may fire before consent signal propagates (async timing issues)
- Scanner misses dynamically loaded cookies (set by JS after page interaction)
- Accessibility issues in older widget versions (missing ARIA labels, poor keyboard nav)

### TrustArc (formerly TRUSTe)
**Positive:** Enterprise-focused, strong privacy program management
**Common issues:**
- Consent manager interface heavy and slow-loading
- Historical "implied consent" configurations don't meet current GDPR standards
- Complex implementation requiring significant developer involvement
- Preference center UI confusing for end users
- Integration with modern frameworks (React, Next.js) problematic

### Secure Privacy
**Positive:** Multiple regulation support, geo-targeted banners
**Common issues:**
- Smaller market share = less third-party audit coverage
- Cookie scanning completeness varies for SPAs with dynamic content
- Some reported issues with Google Consent Mode integration
- Banner accessibility inconsistent across themes/templates
- Iframe-based implementation creates testing challenges (see separate raw source)
- Documentation gaps for advanced configuration

## Cross-CMP Failure Modes

| # | Failure Mode | Description | Detection Method |
|---|-------------|-------------|-----------------|
| 1 | **Race condition** | Tracking scripts fire before CMP blocks them | Check cookies immediately on page load (before banner interaction) |
| 2 | **Tag manager bypass** | Scripts in GTM/other tag managers evade CMP blocking | Monitor network requests for tracking domains pre-consent |
| 3 | **Script chain leakage** | Blocked script already loaded child script that sets cookies | Full network request audit pre-consent |
| 4 | **Iframe cookie leakage** | Third-party iframes set cookies independently of CMP | Capture ALL cookies including third-party domains |
| 5 | **Server-side cookies** | `Set-Cookie` headers bypass client-side CMP | Check response headers for tracking cookies |
| 6 | **Consent desynchronization** | Consent cookie expires but tracking cookies remain | Test with expired consent state |
| 7 | **CDN/cache issues** | Cached pages include tracking scripts despite CMP | Test with cache-busting headers |
| 8 | **Consent string corruption** | TCF TC string becomes malformed | Parse and validate `euconsent-v2` cookie |
| 9 | **Undeclared cookies** | Actual cookies exceed CMP's declared inventory | Compare CMP declarations vs. actual cookies |
| 10 | **Missing prior blocking** | CMP records choice but doesn't actually block scripts | Verify by checking script execution, not just consent state |
| 11 | **SPA navigation** | Cookie behavior differs on client-side vs. full page loads | Test across different navigation patterns |
| 12 | **Service Worker interference** | Service workers cache cookies or bypass consent | Check SW registrations and cached responses |
| 13 | **Shadow DOM** | CMP uses Shadow DOM, selectors can't pierce it | Use special selectors or Playwright's piercing locators |

## Key Sources
- Santos et al. (2021): "Cookie Banners, What's the Purpose?" — Proceedings of the Web Conference
- Nouwens et al. (2020): "Dark Patterns after the GDPR" — CHI Conference
- Matte et al. (2020): "Do Cookie Banners Respect my Choice?" — IEEE S&P
