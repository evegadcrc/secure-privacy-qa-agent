---
title: Prior Consent (Pre-Consent Cookie Blocking)
type: concept
tags: [consent, cookies, testing, eprivacy, gdpr]
sources: [raw/eprivacy-directive.md, raw/gdpr-consent-requirements.md, raw/cnil-enforcement.md]
created: 2026-04-13
updated: 2026-04-13
---

# Prior Consent (Pre-Consent Cookie Blocking)

The principle that **no non-essential cookies may be placed on a user's device before they give explicit consent.** This is the single most important compliance requirement and the most commonly violated.

## Legal Basis

- **[[eprivacy-directive]]** Article 5(3) — consent required before storing/accessing information on terminal equipment
- **[[gdpr]]** Article 4(11) — defines what constitutes valid consent
- **[[planet49]]** — confirmed pre-ticked boxes are not consent
- **[[cnil]]** — has fined Microsoft 60M EUR specifically for pre-consent cookies

## What "Before Consent" Means

When a user first visits a website with a clean browser (no prior consent cookie):
1. The page loads and the consent banner appears
2. **At this point — before the user clicks anything** — only [[strictly-necessary-cookies]] should exist
3. No analytics cookies (`_ga`, `_gid`)
4. No marketing cookies (`_gcl_au`, `_fbp`, `IDE`)
5. No social media cookies
6. No third-party tracking network requests

## Why This Is the #1 Violation

Academic research (Santos et al. 2021) found that **up to 65% of websites** set tracking cookies regardless of user choice. Common causes:

1. **Race condition** — tracking scripts fire before the CMP blocks them
2. **Tag manager bypass** — scripts in GTM evade CMP blocking
3. **Script chain leakage** — blocked script already loaded a child script
4. **Server-side cookies** — `Set-Cookie` headers bypass client-side CMP
5. **Missing prior blocking** — CMP records consent but doesn't actually block scripts

See [[testing-architecture]] for the exact testing protocol.

## Our Audit Finding

Our QA agent found `_gcl_au` (Google Ads) and `test_cookie` (DoubleClick) on [[secure-privacy|secureprivacy.ai]] **before consent** — their own CMP failing to block cookies on their own site.

## Testing Protocol

1. Launch browser with **clean profile**
2. Navigate to target URL
3. Wait 2-3 seconds for scripts to load
4. **Before ANY banner interaction**, capture all cookies
5. Classify each cookie using [[cookie-categories|known patterns]]
6. Any non-necessary cookie = **CRITICAL violation**

Also monitor: network requests to tracking domains, localStorage writes, sessionStorage writes.

## Jurisdictional Variations

| Jurisdiction | Prior Blocking Required? |
|-------------|------------------------|
| EU ([[gdpr]] + [[eprivacy-directive]]) | **Yes** — mandatory |
| UK (PECR + UK GDPR) | **Yes** — mandatory |
| California ([[ccpa-cpra]]) | No — opt-out model |
| Brazil ([[lgpd]]) | Not strictly — no ePrivacy equivalent |
| Thailand (PDPA) | **Yes** — GDPR-aligned |
| India (DPDPA) | **Yes** — GDPR-aligned |

## See Also

- [[eprivacy-directive]] — the law requiring prior consent
- [[strictly-necessary-cookies]] — the only cookies exempt
- [[cookie-categories]] — how to classify detected cookies
- [[secure-privacy]] — our audit findings
- [[compliance-audit-checklist]] — criterion C1
- [[enforcement-landscape]] — cases involving pre-consent violations
