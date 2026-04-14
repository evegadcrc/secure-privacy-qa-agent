---
title: Compliance Audit Checklist
type: synthesis
tags: [testing, compliance, cookies, consent, audit]
sources: [raw/gdpr-consent-requirements.md, raw/eprivacy-directive.md, raw/edpb-consent-guidelines.md, raw/edpb-dark-patterns-guidelines.md, raw/ccpa-cpra-requirements.md, raw/dark-patterns-detection.md, raw/automated-testing-methodology.md]
created: 2026-04-13
updated: 2026-04-13
---

# Compliance Audit Checklist

The master reference for all checks our QA agent performs, organized by severity. Each criterion links to its legal basis and testing approach.

## CRITICAL — Legal violations requiring immediate fix

| ID | Check | Legal Basis | Automated |
|----|-------|-------------|-----------|
| **C1** | No tracking cookies before consent | [[eprivacy-directive\|ePrivacy]] Art 5(3) | Yes — [[prior-consent]] protocol |
| **C2** | Reject button at first layer | [[edpb]] 03/2022, [[cnil]] enforcement | Yes — DOM check |
| **C3** | No pre-ticked non-essential categories | [[planet49]], [[edpb]] 05/2020 | Yes — toggle state check |
| **C4** | Tracking cookies removed after rejection | [[eprivacy-directive\|ePrivacy]] Art 5(3) | Yes — post-reject cookie capture |
| **C5** | Third-party scripts blocked before consent | [[eprivacy-directive\|ePrivacy]] Art 5(3) | Yes — network monitoring |

## MAJOR — Significant compliance risk

| ID | Check | Legal Basis | Automated |
|----|-------|-------------|-----------|
| **M1** | Equal visual prominence (accept/reject) | [[edpb]] 03/2022, [[dark-patterns]] | Partial — CSS comparison + vision |
| **M2** | Click parity (accept/reject same clicks) | [[edpb]] 03/2022, [[cnil]] | Yes — interaction counting |
| **M3** | [[Consent withdrawal]] mechanism exists | [[gdpr]] Art 7(3) | Yes — DOM search post-dismiss |
| **M4** | Withdrawal as easy as giving consent | [[gdpr]] Art 7(3) | Yes — click counting |
| **M5** | Consent record stored | [[gdpr]] Art 7(1) | Yes — consent cookie check |
| **M6** | Granular [[cookie-categories\|category]] consent | [[gdpr]] Art 4(11) "specific" | Yes — preference panel inspection |
| **M7** | Clear, non-manipulative language | [[edpb]] 03/2022, [[dark-patterns]] | Partial — LLM analysis |
| **M8** | [[Global privacy control\|GPC]] signal honored (US) | [[ccpa-cpra\|CCPA/CPRA]], state laws | Yes — GPC header testing |
| **M9** | "Do Not Sell/Share" link (US) | [[ccpa-cpra\|CCPA/CPRA]] | Yes — DOM/link search |
| **M10** | Post-rejection script blocking | [[eprivacy-directive\|ePrivacy]] Art 5(3) | Yes — network monitoring |

## MINOR — Best practice improvements

| ID | Check | Legal Basis | Automated |
|----|-------|-------------|-----------|
| **m1** | Privacy/cookie policy link in banner | [[planet49]], ePrivacy | Yes — link detection |
| **m2** | Cookie purpose explanation on banner | [[gdpr]] "informed" consent | Partial — LLM analysis |
| **m3** | Cookie lifetime + third-party disclosure | [[planet49]] | Manual — policy review |
| **m4** | Secure cookie attributes (Secure, HttpOnly, SameSite) | Security best practice | Yes — cookie inspection |
| **m5** | Reasonable cookie lifetimes | [[cnil]] guidance (13mo max) | Yes — expiry check |
| **m6** | Consent persists across sessions | [[gdpr]], [[ccpa-cpra\|CCPA]] | Yes — return visit test |
| **m7** | [[iab-tcf\|TCF]] API present and functional | TCF 2.2 | Yes — `__tcfapi` check |
| **m8** | Banner responsive design | Best practice | Yes — viewport testing |

## Jurisdiction-Specific Application

Not all checks apply everywhere. See [[opt-in-vs-opt-out]] and [[global-law-comparison]].

| Check | EU | UK | California | US States | Brazil |
|-------|----|----|-----------|-----------|--------|
| C1 (prior blocking) | Required | Required | N/A | N/A | Recommended |
| C2 (reject button) | Required | Required | N/A | N/A | Recommended |
| M8 (GPC) | N/A | N/A | Required | Varies | N/A |
| M9 (DNSS link) | N/A | N/A | Required | Varies | N/A |

## See Also

- [[testing-architecture]] — how these checks are implemented
- [[enforcement-landscape]] — what gets enforced in practice
- [[dark-patterns]] — the UX patterns to detect
- [[prior-consent]] — the most critical check
- [[cookie-categories]] — how to classify detected cookies
