---
title: Enforcement Landscape
type: synthesis
tags: [enforcement, cnil, ftc, ccpa, gdpr, cookies]
sources: [raw/cnil-enforcement.md, raw/us-enforcement-actions.md, raw/planet49-ruling.md]
created: 2026-04-13
updated: 2026-04-13
---

# Enforcement Landscape

Cross-cutting analysis of cookie consent enforcement actions worldwide. These cases define what gets penalized in practice and directly inform our [[compliance-audit-checklist|audit priorities]].

## Landmark Cases

### EU Enforcement

| Case | DPA | Fine | Year | Violation | Our Test |
|------|-----|------|------|-----------|----------|
| **Google** | [[cnil]] | 150M EUR | 2021 | No equally easy reject | C2, M1, M2 |
| **Facebook** | [[cnil]] | 60M EUR | 2021 | Only "Accept" and "Manage" | C2 |
| **Microsoft** | [[cnil]] | 60M EUR | 2022 | Pre-consent cookies on Bing | C1, C5 |
| **TikTok** | [[cnil]] | 5M EUR | 2022 | No equal reject + insufficient info | C2, m2 |
| **Criteo** | [[cnil]] | 40M EUR | 2023 | Cannot demonstrate consent | M5 |
| **[[planet49\|Planet49]]** | CJEU | Ruling | 2019 | Pre-ticked boxes | C3 |
| **IAB Europe** | Belgian DPA | Ruling | 2022 | TC String is personal data | m7 |

### US Enforcement

| Case | Agency | Fine | Year | Violation | Our Test |
|------|--------|------|------|-----------|----------|
| **Sephora** | CA AG | $1.2M | 2022 | Failed to honor [[global-privacy-control\|GPC]] | M8 |
| **BetterHelp** | FTC | $7.8M | 2023 | Tracking pixels sharing health data | C1, C4 |
| **GoodRx** | FTC | $1.5M | 2023 | Health data via tracking cookies | C1 |
| **Avast** | FTC | $16.5M | 2024 | Selling browsing data from cookies | M9 |
| **Epic Games** | FTC | $520M | 2022 | [[dark-patterns\|Dark patterns]] + [[coppa\|COPPA]] | M7, COPPA |
| **DoorDash** | CA AG | Undisclosed | 2023 | Improper data sales | M9 |

## Enforcement Patterns

### What Gets Enforced Most

1. **[[Prior consent]] violations** — tracking cookies before consent (Microsoft, BetterHelp, GoodRx)
2. **Asymmetric reject/accept UI** — reject harder than accept (Google, Facebook, TikTok)
3. **[[Global privacy control|GPC]] non-compliance** — primary US enforcement vector (Sephora)
4. **Consent proof failures** — cannot demonstrate valid consent (Criteo)
5. **[[Dark patterns]]** — increasingly codified and enforced (Epic Games, [[ccpa-cpra|CPRA]])
6. **Sensitive data leakage** — health/financial data via tracking pixels (BetterHelp, GoodRx)

### What Gets Enforced Less (So Far)

- [[Cookie walls]] — some enforcement (Italy) but less consistent
- [[Consent withdrawal]] — rarely the primary violation cited
- [[Strictly necessary cookies|Over-classification]] of necessary cookies — flagged in guidance but few direct fines
- Accessibility of consent banners — emerging area

### Trend: Increasing Severity

- **2019**: Planet49 was a ruling, not a fine
- **2021-2022**: 60-150M EUR fines from [[cnil]]
- **2022-2023**: US states joining enforcement (Sephora precedent)
- **2024+**: CPPA actively enforcing, more states mandating GPC, EAA adding accessibility

## Mapping to Our Audit

Our [[compliance-audit-checklist]] priorities are directly informed by enforcement:

| Priority | Basis |
|----------|-------|
| C1 (pre-consent cookies) | Microsoft 60M EUR, BetterHelp $7.8M |
| C2 (reject at first layer) | Google 150M EUR, Facebook 60M EUR |
| C3 (no pre-ticked boxes) | Planet49 ruling |
| M5 (consent record) | Criteo 40M EUR |
| M8 (GPC honored) | Sephora $1.2M |

## Key Insight

The enforcement pattern shows a clear priority: **DPAs focus on what they can easily verify** — pre-consent cookies and banner design. This aligns with what our automated tool can test. The highest-fined violations (C1, C2) are exactly the checks our QA agent performs best.

## See Also

- [[cnil]] — most active enforcer
- [[ccpa-cpra]] — US enforcement framework
- [[planet49]] — foundational ruling
- [[dark-patterns]] — increasingly enforced
- [[compliance-audit-checklist]] — our test criteria mapped to cases
- [[global-privacy-control]] — Sephora precedent
