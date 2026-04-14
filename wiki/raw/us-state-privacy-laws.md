---
title: US State Privacy Laws — Cookie and Consent Requirements
type: source
tags: [us-state-laws, cookies, consent, us, gpc]
date_added: 2026-04-13
authority: Various US state legislatures
---

# US State Privacy Laws — Cookie and Consent Requirements

All US state privacy laws follow an **opt-out model** (not opt-in like GDPR). None require a cookie consent banner in the EU sense, but they do require opt-out mechanisms for targeted advertising and data sales.

## Colorado Privacy Act (CPA) — Effective July 1, 2023

- Consumers can opt out of: targeted advertising, sale of personal data, profiling
- **Universal opt-out mechanism**: Colorado was one of the first states to **require** businesses to honor universal opt-out signals (like GPC) — mandatory from **July 1, 2024**
- Controllers must conduct data protection assessments for targeted advertising
- Cookies used for targeted advertising trigger opt-out rights
- If a user sends an opt-out signal, targeted advertising cookies must not fire

**Statute:** C.R.S. 6-1-1301+

## Virginia Consumer Data Protection Act (VCDPA) — Effective January 1, 2023

- Consumers can opt out of: targeted advertising, sale of personal data, profiling
- **No requirement to honor universal opt-out signals (GPC)** — Virginia explicitly did not include this
- No specific cookie banner requirement
- Consent required for processing **sensitive data** (similar categories to CPRA)
- Less prescriptive than CCPA/CPRA overall

**Statute:** Va. Code 59.1-575+

## Connecticut Data Privacy Act (CTDPA) — Effective July 1, 2023

- Consumers can opt out of: targeted advertising, sale of personal data, profiling
- **Must honor universal opt-out mechanisms** (like GPC) starting **January 1, 2025**
- Specifically states businesses must treat opt-out preference signals as valid opt-out requests
- One of the stronger state laws after California

**Statute:** Public Act 22-15

## Utah Consumer Privacy Act (UCPA) — Effective December 31, 2023

- **Most business-friendly** of state laws
- Opt-out rights for: sale of personal data, targeted advertising
- **No requirement to honor universal opt-out signals**
- **No private right of action**
- Higher applicability thresholds ($25M revenue AND 100,000 consumers, or 50% revenue from sale + 25,000 consumers)
- Minimal cookie-specific requirements

## Texas Data Privacy and Security Act (TDPSA) — Effective July 1, 2024

- Opt-out model, must recognize universal opt-out mechanisms starting **January 1, 2025**
- Broad applicability (no revenue threshold)
- Controller must respond to opt-out within reasonable time

## Oregon Consumer Privacy Act (OCPA) — Effective July 1, 2024

- Must honor universal opt-out mechanisms
- Includes nonprofit organizations (unusual among state laws)
- Strong enforcement by state AG

## Montana Consumer Data Privacy Act — Effective October 1, 2024

- Must honor universal opt-out mechanisms
- Low applicability threshold (50,000 consumers or revenue from data sale)

## Other States (enacted 2024-2025)

Delaware, New Hampshire, New Jersey, Nebraska, Maryland, Minnesota, Indiana, Kentucky, Tennessee, Rhode Island, Iowa — all enacted privacy laws with varying effective dates. Most follow the Colorado/Connecticut pattern with universal opt-out signal requirements.

## Summary Matrix

| State | Opt-Out Right | Must Honor GPC | Sensitive Data Consent | Effective |
|-------|--------------|----------------|----------------------|-----------|
| California (CCPA/CPRA) | Yes | Yes (mandatory) | Yes (limit use link) | 2020/2023 |
| Colorado | Yes | Yes (from July 2024) | Yes | July 2023 |
| Virginia | Yes | No | Yes | Jan 2023 |
| Connecticut | Yes | Yes (from Jan 2025) | Yes | July 2023 |
| Utah | Yes | No | No | Dec 2023 |
| Texas | Yes | Yes (from Jan 2025) | Yes | July 2024 |
| Oregon | Yes | Yes | Yes | July 2024 |
| Montana | Yes | Yes | Yes | Oct 2024 |

## Key Takeaway for QA Testing

For US-targeted sites, the primary automated checks are:
1. Presence of opt-out mechanism (link or banner)
2. GPC signal honored (for CA, CO, CT, TX, OR, MT)
3. Tracking cookies removed after opt-out
4. No dark patterns in opt-out flow
