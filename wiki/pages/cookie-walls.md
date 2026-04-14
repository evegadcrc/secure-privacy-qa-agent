---
title: Cookie Walls
type: concept
tags: [cookie-walls, consent, gdpr, dark-patterns]
sources: [raw/edpb-consent-guidelines.md, raw/cnil-enforcement.md, raw/germany-ttdsg.md]
created: 2026-04-13
updated: 2026-04-13
---

# Cookie Walls

A **cookie wall** blocks access to website content until the user accepts cookies. This practice is generally considered a violation of [[gdpr]] consent requirements because consent is not "freely given" when the alternative is no access.

## Legal Status

### EDPB Position (Guidelines 05/2020)
- Cookie walls are **presumptively invalid** — consent is not freely given if access is conditional
- Not per se prohibited, but the controller must demonstrate a **genuine equivalent alternative**
- A paid ad-free version *may* be acceptable in some member states (debated)

### CNIL (France)
- Cookie walls are **generally not permitted**
- Conditioning access on acceptance = invalid consent
- Narrow exceptions possible but rarely accepted

### Germany (DSK)
- **Strict prohibition** — cookie walls are non-compliant regardless of alternatives
- Stricter than some other member states that allow "pay or consent" models

### Italy (Garante)
- Multiple fines for cookie walls
- Content access must not be conditioned on cookie acceptance

## "Pay or Consent" Model

Some publishers (notably in Austria, Germany, and the Netherlands) offer a choice: accept cookies for free access, or pay a subscription for cookie-free access. This is controversial:

**Arguments for validity:**
- Users have a genuine alternative
- Publishers need revenue (ads require cookies)
- EDPB leaves the door open

**Arguments against:**
- Financial barrier is not a "genuine" alternative for most users
- Creates a two-tier privacy system (privacy as a luxury)
- German DSK explicitly rejects this model

## Detection in QA Testing

1. After the banner appears, check if page content is visible/accessible
2. Dismiss the banner without consenting (close or attempt to navigate)
3. Check if content becomes hidden, blocked, or overlaid
4. Check for paywall redirect after refusing cookies

## Impact on Consent Validity

If a cookie wall is detected, **all consent given through that mechanism is potentially invalid** under [[gdpr]]. This affects every other test criterion — if consent isn't freely given, the entire compliance framework collapses.

## See Also

- [[gdpr]] — "freely given" consent requirement
- [[edpb]] — presumptive invalidity position
- [[dark-patterns]] — cookie walls as "forced action"
- [[cnil]] — strict prohibition in France
- [[compliance-audit-checklist]] — impacts the "freely given" assessment
