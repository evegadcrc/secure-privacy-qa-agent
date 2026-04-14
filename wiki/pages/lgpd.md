---
title: LGPD (Brazil)
type: entity
tags: [lgpd, brazil, cookies, consent, global-laws]
sources: [raw/lgpd-brazil.md]
created: 2026-04-13
updated: 2026-04-13
---

# LGPD (Lei Geral de Proteção de Dados)

**Brazilian Law 13,709/2018** — Brazil's comprehensive data protection law. Effective September 2020.

## Consent Standard

"Free, informed, and unambiguous manifestation" — similar to [[gdpr]] but with key differences for cookies.

## Key Differences from GDPR

| Aspect | GDPR + ePrivacy | LGPD |
|--------|----------------|------|
| Cookie-specific law | Yes ([[eprivacy-directive]]) | No equivalent |
| Prior blocking required | Yes (ePrivacy Art 5(3)) | Not strictly |
| Legitimate interest for analytics | Generally no | More permissive |
| Consent granularity | Per purpose | Per purpose (Art 8§4) |
| Withdrawal ease | As easy as giving | As easy as giving (Art 8§5) |

The critical difference: **LGPD has no ePrivacy equivalent.** The strict "no cookies before consent" rule comes from ePrivacy, not GDPR itself. Without this, LGPD takes a more flexible approach to cookies.

## Practical Implications

- **Analytics cookies** may be permissible under legitimate interest (ANPD has been lenient)
- **Marketing cookies** still require consent (involves personal data processing)
- **Best practice**: display a consent banner with opt-out, even if not strictly mandated
- Geo-targeting should serve a different banner to Brazilian visitors vs. EU visitors

## Enforcement

The ANPD (Autoridade Nacional de Proteção de Dados) has been less aggressive on cookie enforcement than EU DPAs, focusing more on data breach notifications and general compliance.

## See Also

- [[gdpr]] — the model LGPD was based on
- [[opt-in-vs-opt-out]] — LGPD sits between the two models
- [[global-law-comparison]] — how LGPD compares to other global laws
- [[cookie-categories]] — which categories need consent under LGPD
