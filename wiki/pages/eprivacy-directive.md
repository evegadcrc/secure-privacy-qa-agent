---
title: ePrivacy Directive (Cookie Law)
type: entity
tags: [eprivacy, eu, cookies, consent]
sources: [raw/eprivacy-directive.md]
created: 2026-04-13
updated: 2026-04-13
---

# ePrivacy Directive

**Directive 2002/58/EC** (as amended by 2009/136/EC) — the EU's cookie-specific regulation, commonly called the "Cookie Law."

## Core Rule: Article 5(3)

> Storing or accessing information on a user's device requires **prior consent**, with clear and comprehensive information about purposes.

This is the legal basis for requiring cookie consent banners across the EU. It is **lex specialis** to [[gdpr]] — meaning it takes precedence for the specific act of placing cookies.

## The Strictly Necessary Exemption

The only cookies exempt from consent are those [[strictly-necessary-cookies|strictly necessary]] to provide a service the user explicitly requested:
- Session cookies, auth tokens, CSRF tokens
- Load balancing cookies
- Consent preference cookies

Everything else — analytics, marketing, social, functional preferences — requires consent. See [[cookie-categories]] for the full breakdown.

## Critical Legal Principle: No Legitimate Interest

Unlike [[gdpr]] which offers six legal bases for processing, ePrivacy Article 5(3) provides **only one basis for placing non-essential cookies: consent.** There is no "legitimate interest" shortcut for cookies.

This is why even analytics cookies (like Google Analytics) require consent in the EU, despite arguments about legitimate interest.

## Implementation Across Member States

Each EU member state transposed Article 5(3) into national law:

| Country | Implementation | Notes |
|---------|---------------|-------|
| Germany | [[germany-ttdsg\|TTDSG Section 25]] (2021) | Strict interpretation; cookie walls banned |
| France | [[cnil]] guidelines (2020) | Most active enforcement; symmetric choice required |
| UK | PECR Regulation 6 (post-Brexit) | Enforced by [[ico]] |
| Italy | Garante guidelines | Cookie wall enforcement |
| Spain | LSSI | |

## Proposed ePrivacy Regulation

A regulation (directly applicable, no national transposition) was proposed in 2017 to replace the Directive but has been stalled. As of 2026, the Directive remains in force.

## Relationship to Our Testing

The ePrivacy Directive is the reason our QA agent's **most critical test** is [[prior-consent|pre-consent cookie blocking]]. Any non-essential cookie set before the user clicks "Accept" is a direct violation of Article 5(3).

## See Also

- [[gdpr]] — defines the consent standard referenced by ePrivacy
- [[prior-consent]] — the testing criterion derived from Article 5(3)
- [[strictly-necessary-cookies]] — the exemption category
- [[planet49]] — CJEU ruling clarifying Article 5(3) consent
- [[cnil]] — most active enforcer of ePrivacy cookie rules
