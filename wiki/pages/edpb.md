---
title: EDPB (European Data Protection Board)
type: entity
tags: [edpb, eu, gdpr, consent, dark-patterns]
sources: [raw/edpb-consent-guidelines.md, raw/edpb-dark-patterns-guidelines.md]
created: 2026-04-13
updated: 2026-04-13
---

# EDPB (European Data Protection Board)

The EU body that coordinates data protection enforcement across member states and issues binding guidelines interpreting [[gdpr]].

## Key Guidelines for Cookie Consent

### Guidelines 05/2020 on Consent
The definitive interpretation of GDPR consent:
- **Scrolling/browsing ≠ consent** — cannot be distinguished from normal activity
- **[[Cookie walls]] presumptively invalid** — consent not freely given if access is conditional
- **No pre-ticked boxes** — confirmed by [[planet49]]
- **Bundled consent invalid** — must be granular per purpose (see [[cookie-categories]])
- **[[Consent withdrawal]]** must be as easy as giving consent (comparable clicks)
- **Consent records** must capture: timestamp, choices, banner version, mechanism

### Guidelines 03/2022 on Dark Patterns
Six categories of [[dark-patterns|deceptive design patterns]]:

1. **Overloading** — continuous prompting, privacy maze
2. **Skipping** — deceptive snugness (pre-ticked), misdirection
3. **Stirring** — emotional steering, hidden-in-plain-sight
4. **Hindering** — dead ends, longer-than-necessary, misleading info
5. **Fickle** — lacking hierarchy, ambiguous wording
6. **Left in the dark** — conflicting info, language discontinuity

**Specific cookie banner mandates:**
- Accept and reject at the **same layer**
- **Equal visual prominence** for both
- "Manage preferences" alone is NOT sufficient — direct reject required
- Pre-selected categories = dark pattern

## Impact on Our Testing

EDPB guidelines directly inform our audit criteria:
- **C2** (reject at first layer) ← Guidelines 03/2022
- **C3** (no pre-ticked boxes) ← Guidelines 05/2020 + [[planet49]]
- **M1** (equal prominence) ← Guidelines 03/2022
- **M2** (click parity) ← Guidelines 03/2022
- **M5** (consent record) ← Guidelines 05/2020
- **M6** (granular consent) ← Guidelines 05/2020

## See Also

- [[gdpr]] — the regulation EDPB interprets
- [[dark-patterns]] — the concept defined by Guidelines 03/2022
- [[planet49]] — the ruling EDPB guidelines build upon
- [[cnil]] — most active national enforcer
- [[prior-consent]] — requirement derived from these guidelines
