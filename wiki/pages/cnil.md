---
title: CNIL (France)
type: entity
tags: [cnil, enforcement, france, eu, cookies]
sources: [raw/cnil-enforcement.md]
created: 2026-04-13
updated: 2026-04-13
---

# CNIL (Commission Nationale de l'Informatique et des Libertes)

France's data protection authority — the **most active DPA globally** on cookie consent enforcement.

## Why CNIL Matters

CNIL has imposed the largest cookie-specific fines in history and established de facto standards for the entire EU through their enforcement actions and guidelines.

## Core Cookie Requirements (Deliberation 2020-091)

1. **No cookies before consent** — [[prior-consent]] is mandatory
2. **Symmetric choices** — "Refuse All" must be at same level as "Accept All" (see [[dark-patterns]])
3. **Continued browsing ≠ consent** — scrolling/navigating is not affirmative action
4. **No [[cookie-walls]]** — conditioning access on acceptance is generally invalid
5. **Banner must persist** — no auto-dismiss before user acts
6. **[[Consent withdrawal]] mechanism** must be always accessible
7. **Cookie lifetime**: consent cookie max 13 months; re-prompt max 6 months

## Analytics Exception

CNIL uniquely allows first-party analytics **without consent** if:
- Limited to aggregate audience measurement
- Anonymized IP
- No cross-site tracking
- No third-party data sharing
- Limited retention

Applies to properly configured **Matomo** but **NOT Google Analytics**.

## Major Enforcement Actions

| Target | Fine | Year | Violation |
|--------|------|------|-----------|
| **Google** | 150M EUR | 2021 | No equally easy refuse mechanism |
| **Facebook** | 60M EUR | 2021 | Only "Accept" and "Manage" — no reject |
| **Microsoft** | 60M EUR | 2022 | Cookies before consent on Bing; no equal reject |
| **Criteo** | 40M EUR | 2023 | Could not demonstrate valid consent |
| **TikTok** | 5M EUR | 2022 | No equal refuse; insufficient info |

See [[enforcement-landscape]] for the full analysis.

## Impact on Our Testing

CNIL's enforcement directly maps to our audit criteria:
- **Google/Facebook fines** → we test for reject button at first layer
- **Microsoft fine** → we test [[prior-consent|pre-consent cookies]]
- **Criteo fine** → we test consent record storage

## See Also

- [[edpb]] — coordinates EU-wide guidance
- [[dark-patterns]] — CNIL's strict enforcement against asymmetric UI
- [[prior-consent]] — CNIL's primary enforcement target
- [[enforcement-landscape]] — all enforcement cases analyzed
- [[ico]] — UK's equivalent DPA
