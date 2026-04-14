---
title: Consent Withdrawal
type: concept
tags: [consent, gdpr, cookies, testing]
sources: [raw/gdpr-consent-requirements.md, raw/edpb-consent-guidelines.md]
created: 2026-04-13
updated: 2026-04-13
---

# Consent Withdrawal

The right to **change or revoke** previously given cookie consent. Must be as easy as giving consent.

## Legal Basis

- **[[gdpr]] Article 7(3)**: "The data subject shall have the right to withdraw his or her consent at any time... It shall be as easy to withdraw as to give consent."
- **[[edpb]] Guidelines 05/2020** (paragraphs 113-118): withdrawal must be achievable with comparable ease — no more clicks/interactions than giving consent
- **[[lgpd]] Article 8§5**: same principle — revocation process must match consent process

## What "As Easy As" Means in Practice

If giving consent requires **1 click** (clicking "Accept All"), then withdrawing must require **comparable effort**:

**Compliant:**
- Persistent floating icon → opens preference panel → toggle off → save (2-3 clicks)
- Footer link "Cookie Settings" → preference panel → toggle → save (2-3 clicks)

**Non-compliant:**
- Settings buried 4 levels deep in the privacy policy
- Requires emailing the data controller
- Requires creating an account
- No withdrawal mechanism exists at all
- Link labeled ambiguously ("Legal" or "Site Info" instead of "Cookie Settings")

## Withdrawal Mechanism Requirements

1. **Persistent visibility** — always accessible after banner dismissal (floating icon, footer link, or similar)
2. **Clear labeling** — "Cookie Settings," "Manage Cookies," "Cookie Preferences" — not hidden under generic labels
3. **Shows current state** — when opened, displays current consent choices (which categories are ON/OFF)
4. **Actually works** — toggling off a category must delete/block the relevant cookies
5. **Click parity** — comparable number of steps as giving consent

## Testing Approach

1. Give consent (Accept All)
2. Verify tracking cookies are set
3. Find the withdrawal mechanism (floating icon, footer link)
4. Open it and verify current consent state is shown
5. Withdraw consent (toggle all off, save)
6. Verify tracking cookies are **removed**
7. Count clicks: giving consent vs. withdrawing — must be comparable

## Common Failures

- No withdrawal mechanism exists after banner dismissal
- Mechanism exists but is extremely hard to find
- Opening preferences shows all categories as OFF even though cookies are active
- Withdrawing consent doesn't actually delete cookies (CMP records the change but doesn't clean up)
- Withdrawal requires significantly more clicks than consent

## See Also

- [[gdpr]] — Article 7(3) withdrawal requirement
- [[edpb]] — Guidelines 05/2020 interpretation
- [[dark-patterns]] — "hindering" category includes making withdrawal hard
- [[compliance-audit-checklist]] — criteria M3, M4
- [[testing-architecture]] — consent withdrawal test flow
