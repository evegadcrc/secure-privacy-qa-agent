---
title: Secure Privacy (CMP)
type: entity
tags: [secure-privacy, cmp, cookies, iframe, testing]
sources: [raw/secure-privacy-cmp.md, raw/cmp-compliance-issues.md]
created: 2026-04-13
updated: 2026-04-13
---

# Secure Privacy

**Consent Management Platform** (secureprivacy.ai) — the CMP our QA agent is auditing. Founded 2019, US-based.

## Claims

- Compliance with [[gdpr]], [[ccpa-cpra|CCPA/CPRA]], [[lgpd]], and 55+ global privacy laws
- Automated cookie scanning and categorization
- Auto-blocking of scripts until consent
- [[iab-tcf|IAB TCF]] 2.2 support
- Google Consent Mode v2 integration
- [[global-privacy-control|GPC]] signal detection
- Geo-targeted banners per jurisdiction
- DSAR automation, data mapping, policy management

## Technical Architecture

### Iframe-Based Banner
Secure Privacy renders its banner inside an `<iframe id="ifrmCookieBanner">` using `srcdoc`. This is the defining technical characteristic:

1. Website loads `<script src="https://app.secureprivacy.ai/script/<site-id>.js">`
2. Script creates iframe with empty `srcdoc`
3. Banner content (buttons, text) injected asynchronously inside iframe
4. Script blocking via `type` attribute rewriting (`text/javascript` → `text/plain`)
5. Consent stored in first-party cookie + potentially localStorage

### Accessibility
The iframe has `role="application"`, `aria-label="Cookie Banner"`, and `tabindex="0"` — some accessibility hooks but limited compared to direct DOM implementations.

## Audit Findings

### Pre-Consent Cookie Leakage (CRITICAL)
Our audit found `_gcl_au` (Google Ads) and `test_cookie` (DoubleClick) set **before consent** on secureprivacy.ai itself. This is a direct [[eprivacy-directive|ePrivacy]] violation and their own product's failure to block scripts.

Root causes:
- Tracking scripts in HTML before CMP script intercepts
- Auto-blocking doesn't cover all loading methods
- Race condition between script execution and CMP initialization

### Iframe Testing Limitation
Our tool could not interact with buttons inside the iframe, preventing post-rejection verification. This is a known challenge with iframe-based CMPs.

**Solution:** Use Playwright's `frame_locator()`:
```python
frame = page.frame_locator('#ifrmCookieBanner')
await frame.locator('button:has-text("Decline")').click()
```

## See Also

- [[testing-architecture]] — how to handle iframe-based CMPs
- [[prior-consent]] — the critical test Secure Privacy failed
- [[compliance-audit-checklist]] — full checklist for auditing CMPs
- [[dark-patterns]] — what to check in any CMP's banner design
