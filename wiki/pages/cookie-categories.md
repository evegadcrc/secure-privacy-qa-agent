---
title: Cookie Categories
type: concept
tags: [cookies, categorization, consent, testing]
sources: [raw/cookie-categorization-standards.md, raw/iab-tcf-2-2.md]
created: 2026-04-13
updated: 2026-04-13
---

# Cookie Categories

The standard classification system for cookies, determining which require consent and which are exempt.

## The Five Categories

### 1. [[strictly-necessary-cookies|Strictly Necessary]]
Essential for the site to function. **No consent needed** (exempt under [[eprivacy-directive|ePrivacy Art 5(3)]]).
- Session IDs, CSRF tokens, auth cookies, consent preference cookies, load balancers
- Must genuinely be necessary — over-classification is a compliance violation

### 2. Functional / Preferences
Remember user choices not essential to function. **Consent required.**
- Language selection, UI theme, font size, recently viewed
- Some DPAs accept legitimate interest; consent is the safer basis

### 3. Analytics / Statistics
Measure site usage. **Consent generally required.**
- `_ga`, `_gid`, `_gat`, Matomo, Hotjar, Adobe Analytics
- **Exception:** [[cnil]] allows privacy-friendly first-party analytics without consent (anonymized IP, no cross-site, no sharing). Does NOT apply to Google Analytics.

### 4. Marketing / Advertising
Track users for targeted ads. **Explicit consent always required.** Strictest category.
- `_gcl_au`, `_fbp`, `IDE`, DoubleClick, retargeting pixels
- No legitimate interest basis. Involves third-party data sharing.

### 5. Social Media
Enable social integration. **Consent required.**
- Facebook Connect, Twitter widgets, LinkedIn Insight, YouTube embeds
- Often overlaps with marketing; some CMPs merge these

## Default State Rules

| Category | Default | Consent | Can Pre-Check | Must Block |
|----------|---------|---------|---------------|-----------|
| Strictly Necessary | ON | No | N/A | No |
| Functional | OFF | Yes | No | Yes |
| Analytics | OFF | Yes* | No | Yes |
| Marketing | OFF | Yes | No | Yes |
| Social Media | OFF | Yes | No | Yes |

All non-necessary categories must default to **OFF** — pre-checking them violates [[planet49]].

## Known Tracking Patterns

**Analytics:** `_ga`, `_gid`, `_gat`, `__utma/b/c/z`, `_clck`, `_clsk`

**Marketing:** `_gcl_au`, `_gcl_aw`, `_fbp`, `_fbc`, `fr`, `IDE`, `DSID`, `test_cookie`, `_tt_`, `_ttp`, `_pin_unauth`, `NID`, `_uetsid`, `_uetvid`, `li_sugr`, `hubspotutk`, `__hssc/hssrc/hstc`

**Necessary:** `session*`, `PHPSESSID`, `JSESSIONID`, `csrf*`, `xsrf*`, `__cfduid`, `*consent*`, `OptanonConsent`, `euconsent*`

## Audit Rules

1. Tracking cookie found **before consent** → **CRITICAL** (see [[prior-consent]])
2. Tracking cookie found **after rejection** → **CRITICAL**
3. "Unknown" cookie → flag for manual review
4. "Necessary" cookie that looks like analytics/marketing → **MAJOR** (over-classification)
5. Cookie not in CMP's declared inventory → compliance gap

## Google Consent Mode v2

Google's consent signal categories (separate from standard classification):
- `ad_storage` — advertising cookies
- `analytics_storage` — analytics cookies
- `ad_user_data` — user data for advertising
- `ad_personalization` — ad personalization

CMP must correctly map consent choices to these signals.

## See Also

- [[strictly-necessary-cookies]] — deep dive on the exempt category
- [[prior-consent]] — what happens when non-necessary cookies appear too early
- [[planet49]] — no pre-ticked categories
- [[iab-tcf]] — TCF's 11 purposes map to these categories
- [[compliance-audit-checklist]] — testing criteria for cookie behavior
