---
title: Cookie Categorization Standards
type: source
tags: [cookies, categorization, consent, testing]
date_added: 2026-04-13
authority: IAB Europe TCF, ISO conventions, major CMPs
---

# Cookie Categorization Standards

## Standard Categories

### 1. Strictly Necessary Cookies
- **Purpose:** Essential for the website to function (session management, load balancing, security tokens, shopping cart, cookie consent preferences)
- **Consent requirement:** No consent needed — exempt under ePrivacy Article 5(3). Must genuinely be necessary; this category is often abused by over-classifying cookies.
- **Examples:** Session IDs, CSRF tokens, authentication cookies, consent preference cookies
- **Rules:** Cannot include analytics, tracking, or advertising cookies. Should have the shortest reasonable lifetime.

### 2. Functional / Preference Cookies
- **Purpose:** Remember user choices not strictly necessary (language preference, region, UI customization, accessibility settings)
- **Consent requirement:** Consent required under GDPR/ePrivacy. Some DPAs accept "legitimate interest" for basic functionality, but consent is the safer basis.
- **Examples:** Language selection, font size, recently viewed items
- **Lifetime:** Session to 1 year

### 3. Analytics / Statistics Cookies
- **Purpose:** Collect data about how visitors use the website (page views, bounce rate, traffic sources)
- **Consent requirement:** Generally required. Exception: some DPAs (CNIL, Dutch DPA) allow first-party analytics without consent IF properly configured (anonymized IP, no cross-site tracking, no third-party sharing, limited lifetime). This exception applies to Matomo/Piwik but NOT to Google Analytics.
- **Examples:** `_ga`, `_gid`, `_gat`, Matomo, Hotjar, Adobe Analytics
- **Lifetime:** Session to 2 years

### 4. Marketing / Advertising Cookies
- **Purpose:** Track users across websites to build profiles and serve targeted ads
- **Consent requirement:** Explicit consent ALWAYS required. Strictest category. Must be opt-in. No legitimate interest basis.
- **Examples:** `_gcl_au`, `_gcl_aw`, `_fbp`, `IDE`, DoubleClick, retargeting pixels
- **Lifetime:** 30 days to 2 years
- **Special:** Often involves third-party data sharing requiring disclosure of recipients

### 5. Social Media Cookies
- **Purpose:** Enable social media integration (share buttons, embedded content, login via social accounts)
- **Consent requirement:** Consent required. Typically third-party cookies enabling cross-site tracking.
- **Examples:** Facebook Connect, Twitter widgets, LinkedIn Insight, YouTube embeds
- **Note:** Often overlaps with marketing; some CMPs merge these. IAB TCF treats social media tracking as a "special purpose."

## Default State Rules

| Category | Default State | Consent Required | Can Pre-check | Must Block Before Consent |
|----------|--------------|------------------|---------------|---------------------------|
| Strictly Necessary | Active | No | N/A (always on) | Not blocked |
| Functional | Inactive | Yes | No | Must block |
| Analytics | Inactive | Yes* | No | Must block |
| Marketing | Inactive | Yes | No | Must block |
| Social Media | Inactive | Yes | No | Must block |

*Exception for privacy-friendly first-party analytics in some jurisdictions

## Known Tracking Cookie Patterns

### Analytics (consent required)
```
_ga, _gid, _gat, __utma, __utmb, __utmc, __utmz
_clck, _clsk (Microsoft Clarity)
```

### Marketing (consent required)
```
_gcl_au, _gcl_aw (Google Ads conversion)
_fbp, _fbc, fr (Facebook)
_tt_, _ttp (TikTok)
_pin_unauth (Pinterest)
IDE, DSID, test_cookie (DoubleClick/Google Ads)
NID, APISID, SAPISID, SSID, SID (Google general)
_uetsid, _uetvid (Microsoft/Bing)
li_sugr, bcookie, lidc (LinkedIn)
sc_at (Snapchat)
_rdt_uuid (Reddit)
hubspotutk, __hssc, __hssrc, __hstc (HubSpot)
```

### Necessary (no consent needed)
```
session*, PHPSESSID, JSESSIONID, ASP.NET_SessionId
csrf*, xsrf*, token*
__cfduid, cf_clearance (Cloudflare)
*consent*, OptanonConsent, CookieConsent, euconsent*
```

## Classification Rules for Auditing

1. Cookie matching a tracking pattern found BEFORE consent = **CRITICAL violation**
2. Cookie matching a tracking pattern found AFTER rejection = **CRITICAL violation**
3. Cookie classified as "unknown" = flag for **manual review** (may be miscategorized by CMP)
4. "Strictly necessary" cookie that appears to be analytics/marketing = **MAJOR violation** (over-classification abuse)
5. CMP's declared inventory vs. actual cookies found — undeclared cookies are a compliance gap
6. Third-party domain cookies are almost always non-necessary and require consent

## Google Consent Mode v2 Categories

Google uses its own consent signal categories:
- `ad_storage` — consent for advertising cookies
- `analytics_storage` — consent for analytics cookies
- `ad_user_data` — consent for sending user data to Google for advertising
- `ad_personalization` — consent for ad personalization

These must be correctly set by the CMP based on user consent choices.
