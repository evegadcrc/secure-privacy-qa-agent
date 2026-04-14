---
title: Opt-In vs Opt-Out Models
type: comparison
tags: [consent, gdpr, ccpa, cookies]
sources: [raw/gdpr-consent-requirements.md, raw/ccpa-cpra-requirements.md, raw/eprivacy-directive.md]
created: 2026-04-13
updated: 2026-04-13
---

# Opt-In vs Opt-Out Models

The two fundamental approaches to cookie consent, representing the deepest structural difference between EU and US privacy law.

## Side-by-Side Comparison

| Aspect | Opt-In (EU) | Opt-Out (US) |
|--------|-------------|-------------|
| **Default state** | No tracking until consent | Tracking by default |
| **User action needed** | Must actively accept | Must actively refuse |
| **Who** | [[gdpr]] + [[eprivacy-directive]] | [[ccpa-cpra]], US state laws |
| **Banner required** | Yes — must block cookies first | No — opt-out link required |
| **Reject button** | Required at first layer | Not required (opt-out link instead) |
| **Pre-consent cookies** | Violation ([[prior-consent]]) | Permitted |
| **Legal basis** | Consent (Art 6(1)(a)) | Notice + right to opt out |
| **Mechanism** | Cookie consent banner | "Do Not Sell/Share" link + [[global-privacy-control\|GPC]] |

## Why This Matters for Testing

Our QA agent must apply **different test criteria** depending on the jurisdiction:

### For EU/Opt-In Sites
- [[prior-consent]] is the #1 test — no cookies before consent
- Reject button at first layer required
- Equal prominence required ([[dark-patterns]])
- Granular [[cookie-categories|category]] consent
- [[consent-withdrawal]] mechanism

### For US/Opt-Out Sites
- "Do Not Sell or Share" link on homepage
- [[global-privacy-control|GPC]] signal honored
- Tracking removed after opt-out
- No [[dark-patterns]] in opt-out flow
- No [[prior-consent|pre-consent blocking]] required

### For Hybrid Jurisdictions
- [[lgpd]] — consent recommended but legitimate interest accepted for some analytics
- PIPEDA (Canada) — meaningful consent, implied may suffice for non-sensitive
- Quebec (Law 25) — opt-in, GDPR-like

## The Convergence Trend

Despite the structural difference, trends are converging:
- US states increasingly mandate [[global-privacy-control|GPC]] honor (effectively opt-out enforcement)
- [[ccpa-cpra|CPRA]] codified [[dark-patterns]] prohibition (similar to [[edpb]])
- India ([[global-law-comparison|DPDPA]]) and Thailand (PDPA) chose GDPR-like opt-in
- Even in opt-out regimes, industry CMPs often deploy opt-in banners for simplicity

## Geo-Targeting Implications

CMPs like [[secure-privacy]] must serve different banners per jurisdiction:
- EU visitor → full opt-in banner with [[prior-consent|prior blocking]]
- California visitor → opt-out notice with "Do Not Sell" link
- Colorado/Connecticut/Texas visitor → opt-out with GPC mandatory
- Brazil visitor → consent banner recommended (hybrid approach)
- Unregulated visitor → may show no banner

## See Also

- [[gdpr]] — the opt-in framework
- [[ccpa-cpra]] — the opt-out framework
- [[global-law-comparison]] — where each country falls
- [[global-privacy-control]] — the technical opt-out mechanism
- [[compliance-audit-checklist]] — jurisdiction-specific criteria
