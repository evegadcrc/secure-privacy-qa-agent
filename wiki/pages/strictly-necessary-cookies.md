---
title: Strictly Necessary Cookies
type: concept
tags:
  - cookies
  - consent
  - eprivacy
  - necessary
sources:
  - raw/eprivacy-directive.md
  - raw/cookie-categorization-standards.md
created: 2026-04-13
updated: 2026-04-13
---

# Strictly Necessary Cookies

The only [[cookie-categories|category]] of cookies **exempt from consent** under [[eprivacy-directive|ePrivacy Article 5(3)]]. These cookies are essential for the website to function as explicitly requested by the user.

## Definition (Article 29 Working Party, Opinion 04/2012)

A cookie is strictly necessary when it is **indispensable** for a service explicitly requested by the user. The exemption is narrow and often abused.

## What Qualifies

| Cookie Type | Example | Why Exempt |
|------------|---------|-----------|
| Session management | `PHPSESSID`, `JSESSIONID` | User explicitly requests pages; session needed to serve them |
| Authentication | Auth tokens | User explicitly logs in |
| Security | CSRF tokens, `XSRF-TOKEN` | Protects user-requested actions |
| Load balancing | Load balancer cookies | Needed to route user requests |
| Consent preference | `CookieConsent`, `OptanonConsent` | Records the user's own consent choice |
| Shopping cart | Cart session cookies | User explicitly adds items |
| Multimedia player | Player session state | User explicitly plays media |

## What Does NOT Qualify

| Cookie Type | Why NOT Exempt |
|------------|---------------|
| Google Analytics (`_ga`, `_gid`) | Site analytics ≠ service requested by user |
| Marketing (`_fbp`, `_gcl_au`) | Advertising is not user-requested |
| Social media (`fr`, `bcookie`) | Social widgets not explicitly requested |
| A/B testing | Site optimization ≠ user-requested service |
| Personalization/recommendations | Not strictly necessary to provide the base service |
| Third-party analytics | Never strictly necessary |
| Fingerprinting | Not a cookie but same principle — not necessary |

## The Over-Classification Problem

CMPs and site owners sometimes **abuse the "strictly necessary" category** by classifying analytics or functional cookies as necessary to avoid requiring consent. This is a compliance violation:

- [[cnil]] has specifically flagged this practice
- Academic research (Santos et al. 2021) found significant over-classification in CMP inventories
- Our QA agent should flag any cookie classified as "necessary" that matches known tracking patterns

## Lifetime Considerations

Strictly necessary cookies should have the **shortest reasonable lifetime**:
- Session cookies (expire when browser closes) are preferred
- Consent preference cookies: [[cnil]] recommends max 13 months
- Persistent necessary cookies should be justified

## Testing Approach

1. On fresh page load (before any consent), capture all cookies
2. Every cookie present should be classifiable as strictly necessary
3. Cross-reference against known tracking patterns — any match = violation
4. In the CMP's preferences panel, the "Necessary" category should be non-toggleable (always on, greyed out)
5. Flag any "necessary" cookie from a third-party domain — these are suspicious

## See Also

- [[eprivacy-directive]] — the exemption source
- [[cookie-categories]] — all five categories
- [[prior-consent]] — only necessary cookies allowed before consent
- [[compliance-audit-checklist]] — criterion C1 relies on this distinction
