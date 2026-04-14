---
title: CCPA/CPRA (California Privacy Laws)
type: entity
tags: [ccpa, cpra, us, california, cookies, consent]
sources: [raw/ccpa-cpra-requirements.md, raw/us-enforcement-actions.md]
created: 2026-04-13
updated: 2026-04-13
---

# CCPA/CPRA

**California Consumer Privacy Act** (2018) and **California Privacy Rights Act** (2020 ballot, effective 2023) — the strongest US privacy laws.

## Fundamental Model: Opt-Out

Unlike [[gdpr]]'s opt-in model, CCPA/CPRA allows tracking by default. The right is to **opt out**, not to opt in. See [[opt-in-vs-opt-out]] for a detailed comparison.

## Key Requirements for Cookie Compliance

### "Do Not Sell or Share" Link
- Must be on the **homepage**, clear and conspicuous
- Must lead to a working opt-out mechanism
- No account creation required to use it
- Opt-out effectuated within 15 business days

### CPRA Addition: "Sharing"
CPRA added "sharing" (cross-context behavioral advertising) as a regulated activity alongside "selling." This specifically targets ad tech cookies/pixels even without money changing hands.

### "Limit Use of Sensitive PI" Link
Required if the site collects sensitive personal information (including precise geolocation via cookies). Can be combined with "Do Not Sell" into **"Your Privacy Choices."**

### [[dark-patterns|Dark Patterns]] Prohibition
CPRA Section 1798.140(l) defines dark patterns in statute. Any consent obtained through dark patterns is **void.** The CPPA regulations (Section 7004) prohibit confusing language, unnecessary steps, and manipulative design.

### [[global-privacy-control|GPC]] Mandate
CPRA regulations (Section 7025) require businesses to treat GPC (`Sec-GPC: 1`) as a valid opt-out of sale/sharing. Failure to honor GPC was the basis for the [[enforcement-landscape|Sephora $1.2M fine]].

## Enforcement

- **California AG** — primary enforcer pre-CPRA
- **CPPA** (California Privacy Protection Agency) — dedicated agency created by CPRA
- Notable cases: Sephora ($1.2M for GPC), DoorDash (improper data sales)

## Testing Checklist

For sites subject to CCPA/CPRA:
1. "Do Not Sell or Share" link on homepage
2. Working opt-out mechanism
3. [[global-privacy-control|GPC]] signal honored
4. Marketing cookies removed after opt-out
5. No [[dark-patterns]] in opt-out flow

## See Also

- [[opt-in-vs-opt-out]] — how CCPA differs from GDPR
- [[global-privacy-control]] — the legally mandated browser signal
- [[dark-patterns]] — CPRA's statutory prohibition
- [[enforcement-landscape]] — Sephora and other US cases
- [[gdpr]] — contrasting EU approach
