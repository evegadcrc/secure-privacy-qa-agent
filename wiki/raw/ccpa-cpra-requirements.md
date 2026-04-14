---
title: CCPA/CPRA Cookie Consent Requirements
type: source
tags: [ccpa, cpra, cookies, consent, us, california]
date_added: 2026-04-13
authority: California Civil Code 1798.100+; Proposition 24
---

# CCPA/CPRA Cookie Consent Requirements

## Fundamental Difference from GDPR: Opt-Out vs. Opt-In

| Aspect | GDPR/ePrivacy | CCPA/CPRA |
|--------|---------------|-----------|
| Default state | No tracking until consent given (opt-in) | Tracking allowed by default (opt-out) |
| Cookie banner required? | Yes, must block cookies before consent | No banner required; must provide opt-out mechanism |
| "Reject All" button | Required at first layer | Not required; "Do Not Sell/Share" link instead |
| Legal basis | Consent (Art. 6(1)(a) GDPR) | Notice + right to opt out |

## CCPA Core Requirements (Cal. Civ. Code 1798.100+)

### What Constitutes "Personal Information" for Cookies
Cookies that collect unique identifiers, IP addresses, browsing history, or device identifiers constitute "personal information" (Section 1798.140(v)). Most analytics and marketing cookies fall under CCPA scope.

### "Do Not Sell or Share My Personal Information" Link
- Businesses that "sell" or "share" personal information must provide a **clear and conspicuous link** on their homepage
- Link must be titled **"Do Not Sell or Share My Personal Information"**
- "Sell" = exchanging personal information for monetary or other valuable consideration
- "Share" (added by CPRA) = making personal information available to third parties for cross-context behavioral advertising, regardless of monetary exchange
- Link must lead to a working opt-out mechanism
- Opt-out must be effectuated within **15 business days**
- Must **not require account creation** to exercise this right
- Must be present on the **homepage**

## CPRA Amendments (Proposition 24, effective January 2023)

### "Sharing" as a Regulated Activity
The CPRA added "sharing" as separate from "selling." This was critical because many companies argued they weren't "selling" data (no money exchanged) but were sharing it with ad partners via cookies/pixels. "Sharing" specifically targets:
- Programmatic advertising
- Retargeting pixels
- Ad tech cookie syncing
- Cross-context behavioral advertising

### "Limit the Use of My Sensitive Personal Information" Link
- Required if business collects "sensitive personal information"
- Sensitive PI includes: SSN, financial accounts, precise geolocation, racial/ethnic origin, biometric data, health data, sex life/orientation data
- For cookies: **precise geolocation data** collected via cookies/JavaScript is the most relevant
- Businesses may combine both links into **"Your Privacy Choices"** or **"Your California Privacy Choices"**

### Dark Patterns Provisions (Section 1798.140(l))
- CPRA **defines dark patterns in statute**: user interfaces designed to subvert or impair user autonomy or decision-making
- Any consent obtained through dark patterns is **void**
- CPRA Regulations (Section 7004(a)) prohibit: confusing language, unnecessary steps, manipulative design in opt-out flows
- This is one of the first statutory codifications of dark pattern prohibitions

### CPPA (California Privacy Protection Agency)
- Dedicated enforcement agency created by CPRA
- Has rulemaking authority
- Has issued detailed regulations on: dark patterns (Section 7004), opt-out preference signals (Section 7025), consent requirements
- Supplements California AG enforcement

## Technical Requirements for QA Testing

1. **Presence of "Do Not Sell or Share" link** on the homepage
2. **Link functionality** — leads to a working opt-out mechanism
3. **Third-party cookies/tracking after opt-out** — marketing cookies removed or blocked
4. **No dark patterns** in opt-out flow (no confusing language, unnecessary steps, manipulative design)
5. **GPC signal honored** (see separate raw source)
6. **"Limit Use" link** present if sensitive data is collected
7. **Opt-out works without account creation**

## Key Sources
- CCPA: Cal. Civ. Code 1798.100-1798.199.100
- CPRA: Proposition 24
- CPRA Regulations: Title 11, Div. 6, California Code of Regulations
- CPPA enforcement tracker: https://cppa.ca.gov/enforcement/
