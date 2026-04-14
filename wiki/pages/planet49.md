---
title: Planet49 Ruling (CJEU C-673/17)
type: entity
tags: [planet49, cjeu, eu, consent, enforcement]
sources: [raw/planet49-ruling.md]
created: 2026-04-13
updated: 2026-04-13
---

# Planet49 (CJEU C-673/17)

**Landmark ruling** by the Court of Justice of the European Union, decided October 1, 2019. Originated from the German Bundesgerichtshof.

## Facts

Planet49 ran a promotional lottery requiring participants to consent to web tracking via a **pre-ticked checkbox**. The German consumer federation challenged this.

## Holdings

### 1. Pre-ticked Checkboxes ≠ Valid Consent
A checkbox the user must *uncheck* to refuse is not a "clear affirmative action." This ended the practice of defaulting non-essential [[cookie-categories|cookie categories]] to ON.

### 2. Applies to ALL Cookies, Not Just Personal Data
[[eprivacy-directive|ePrivacy Article 5(3)]] protects device integrity, not just personal data. Even cookies containing no personal data require consent.

### 3. Information Must Include Duration and Third-Party Access
"Clear and comprehensive information" requires disclosing:
- **Cookie lifetime/duration**
- **Whether third parties** access the cookies
- **Processing purposes**

### 4. Consent Must Be Unbundled
Consent for a lottery cannot be bundled with consent for cookie tracking. Each purpose requires separate, specific consent.

## Impact on Industry

Planet49 definitively:
- Ended the "implied consent" era across the EU
- Forced all CMPs to implement opt-in models with boxes unchecked
- Required cookie policies to list durations and third-party access
- Became binding precedent for all 27 EU member states
- Was the ruling [[edpb]] Guidelines 05/2020 built upon

## Impact on Our Testing

| Holding | Test Criterion |
|---------|---------------|
| No pre-ticked boxes | **C3** — check default state of toggles |
| Duration disclosure | **m3** — cookie policy must list lifetimes |
| Third-party disclosure | **m3** — must identify third-party access |
| Unbundled consent | **M6** — granular category controls |

## See Also

- [[gdpr]] — consent definition that Planet49 interpreted
- [[eprivacy-directive]] — Article 5(3) at issue in the case
- [[edpb]] — guidelines building on this ruling
- [[dark-patterns]] — pre-ticked boxes now classified as "deceptive snugness"
- [[cnil]] — applied Planet49 principles in enforcement
