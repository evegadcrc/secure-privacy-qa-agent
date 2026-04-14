---
title: IAB Transparency & Consent Framework (TCF)
type: entity
tags: [tcf, iab, consent, advertising, eu]
sources: [raw/iab-tcf-2-2.md]
created: 2026-04-13
updated: 2026-04-13
---

# IAB TCF (Transparency & Consent Framework)

**Industry self-regulatory framework** by IAB Europe — the de facto standard for [[gdpr]] compliance in programmatic advertising. Current version: **TCF 2.2** (mandatory since November 2023).

## Key Principle

TCF is **not law** but is effectively required for EU ad serving since Google and other ad exchanges mandate TCF compliance.

## Technical Components

### TC String (`euconsent-v2`)
Base64-encoded consent record capturing: purposes consented, vendors consented, legal basis, CMP ID, timestamp. Stored as the `euconsent-v2` cookie.

### CMP API (`__tcfapi`)
JavaScript API at `window.__tcfapi`:
- `getTCData` — current consent state
- `addEventListener` — consent change events
- `ping` — CMP availability check

Must be available **before** ad scripts load (stub/loader pattern).

### Global Vendor List (GVL)
Only registered vendors can use TCF. Each vendor declares which purposes and legal bases they use.

## TCF 2.2 Changes (from 2.0)

- **Purpose 1 (device access/storage) requires consent only** — no legitimate interest basis
- Must show vendor **names and count** to users
- No "out-of-band" consent — all consent through the CMP
- Must disclose data categories (e.g., precise geolocation)

## Legal Status

- Belgian DPA found IAB Europe is a joint controller for TC String processing (2022)
- TC String itself constitutes personal data
- Using TCF does not guarantee [[gdpr]] compliance — it's a framework, not a safe harbor

## Testing Approach

Our QA agent should check:
1. `__tcfapi` present on the page
2. TC string parseable and valid
3. Pre-interaction: no consent recorded
4. Post-accept: full consent in TC string
5. Post-reject: no non-essential consent
6. `euconsent-v2` cookie matches API response
7. CMP ID registered on IAB's list

## See Also

- [[gdpr]] — the regulation TCF serves
- [[eprivacy-directive]] — the cookie-specific rules TCF addresses
- [[secure-privacy]] — claims TCF 2.2 support
- [[cookie-categories]] — TCF's 11 purposes map to standard categories
- [[testing-architecture]] — TCF verification protocol
