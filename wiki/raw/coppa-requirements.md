---
title: COPPA Cookie-Specific Requirements
type: source
tags: [coppa, cookies, children, us, ftc]
date_added: 2026-04-13
authority: 15 U.S.C. 6501-6506; FTC COPPA Rule (16 CFR Part 312)
---

# COPPA Cookie-Specific Requirements

## Overview

COPPA (Children's Online Privacy Protection Act) applies to websites and online services:
- **Directed at children under 13**, OR
- That have **actual knowledge** they are collecting data from children under 13

## Persistent Identifiers as Personal Information

Under COPPA, a "persistent identifier" (including cookies, IP addresses, device IDs) that can be used to recognize a user over time and across different sites **is personal information** when used for targeted advertising or sold to third parties.

## Cookie-Specific Rules

### 1. Verifiable Parental Consent Required
Before collecting personal information from children under 13 — including persistent identifiers (cookies) used for purposes other than internal operations.

### 2. Internal Operations Exception
Persistent identifiers used **solely for internal operations** are exempt:
- Maintaining a session
- Frequency capping
- Contextual advertising on the same site (not behavioral/targeted)

If cookie data is shared with third parties or used for behavioral advertising, consent IS required.

### 3. Third-Party Tracking on Child-Directed Sites
Operators of child-directed sites must **not allow third-party ad networks to place tracking cookies** unless they have verifiable parental consent. This is a major enforcement area — many child-directed sites have been fined for allowing Google Analytics, Facebook pixels, etc.

### 4. No Behavioral Advertising Without Consent
Third-party advertising cookies enabling behavioral/targeted advertising on child-directed sites require verifiable parental consent.

## COPPA Updates (2024-2025)

The FTC finalized significant updates to the COPPA Rule effective April 2025:
- Expanded definition of personal information
- Strengthened data minimization requirements
- Added requirements around EdTech and school-authorized collection
- Tightened data retention and security requirements for persistent identifiers
- Extended some coverage to teens 13-16 (proposed)

## QA Testing Implications

If the site targets or may attract children:

1. **Check for third-party tracking cookies** (Google Analytics, Facebook, ad networks) — should NOT be present without verifiable parental consent mechanism
2. **Check for behavioral advertising pixels** — should NOT be present
3. **Session cookies for internal operations** are generally acceptable
4. **Age gate/verification mechanism** should be present if general audience site may attract children
5. **First-party analytics** for internal operations only — may be acceptable without consent

## Key Enforcement Examples

- **Musical.ly/TikTok** (2019): $5.7M fine for collecting children's data without parental consent
- **YouTube/Google** (2019): $170M fine for tracking children on child-directed channels
- **Epic Games/Fortnite** (2022): $275M COPPA component for collecting children's data
- Multiple smaller operators fined for allowing third-party tracking on child-directed sites

## Key Sources
- COPPA: 15 U.S.C. 6501-6506
- FTC COPPA Rule: 16 CFR Part 312
- FTC COPPA FAQ: https://www.ftc.gov/business-guidance/resources/complying-coppa-frequently-asked-questions
