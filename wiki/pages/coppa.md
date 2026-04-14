---
title: COPPA (Children's Online Privacy)
type: entity
tags: [coppa, us, children, cookies, ftc]
sources: [raw/coppa-requirements.md, raw/us-enforcement-actions.md]
created: 2026-04-13
updated: 2026-04-13
---

# COPPA (Children's Online Privacy Protection Act)

**US federal law** (15 U.S.C. 6501-6506) protecting children under 13 online. Enforced by the FTC.

## Cookie-Specific Rules

### Persistent Identifiers = Personal Information
Cookies, IP addresses, and device IDs that can recognize a user over time and across sites **are personal information** under COPPA when used for targeted advertising or sold to third parties.

### Verifiable Parental Consent
Required before collecting personal information from children under 13 — including tracking cookies.

### Internal Operations Exception
Persistent identifiers for **internal operations only** are exempt:
- Session management
- Frequency capping
- Contextual (not behavioral) advertising on the same site

If cookie data is shared with third parties or used for behavioral advertising → consent IS required.

### Third-Party Tracking Ban
Child-directed sites must **not allow** third-party ad networks (Google Analytics, Facebook pixels, etc.) to place tracking cookies without verifiable parental consent. This is a major enforcement area.

## Notable Enforcement

| Case | Fine | Year |
|------|------|------|
| Musical.ly/TikTok | $5.7M | 2019 |
| YouTube/Google | $170M | 2019 |
| Epic Games/Fortnite | $275M | 2022 |

## 2025 Updates

FTC finalized significant COPPA Rule updates:
- Expanded personal information definition
- Strengthened data minimization
- Tightened persistent identifier requirements
- Extended some coverage to teens 13-16

## Testing Implications

If a site targets or may attract children:
1. Check for third-party tracking cookies → should NOT be present
2. Check for behavioral advertising pixels → should NOT be present
3. Look for age gate/verification mechanism
4. Session cookies for internal operations are acceptable

## See Also

- [[enforcement-landscape]] — COPPA enforcement cases
- [[cookie-categories]] — which cookies are problematic for children's sites
- [[ccpa-cpra]] — California's privacy law also has children's provisions
