---
title: IAB Transparency & Consent Framework (TCF) 2.2
type: source
tags: [tcf, iab, consent, cookies, eu, advertising]
date_added: 2026-04-13
authority: IAB Europe
document: TCF v2.2 (released May 2023, mandatory November 2023)
---

# IAB Transparency & Consent Framework (TCF) 2.2

## What It Is

TCF 2.2 is an industry self-regulatory framework developed by IAB Europe to standardize how publishers, advertisers, and ad tech vendors communicate and obtain user consent for data processing under GDPR and the ePrivacy Directive.

**Important:** TCF is NOT law — it is an industry framework. But it is the de facto standard for GDPR compliance in programmatic advertising.

## Key Requirements

### Purposes for Data Processing

TCF defines 11 purposes:
1. Store and/or access information on a device
2. Select basic ads
3. Create a personalised ads profile
4. Select personalised ads
5. Create a personalised content profile
6. Select personalised content
7. Measure ad performance
8. Measure content performance
9. Apply market research to generate audience insights
10. Develop and improve products
11. Use limited data to select content

### Consent vs. Legitimate Interest

For each purpose, vendors declare their legal basis. **TCF 2.2 removed legitimate interest as a legal basis for Purpose 1** ("Store and/or access information on a device") — this means placing cookies ALWAYS requires explicit consent under TCF 2.2.

### Changes in TCF 2.2 vs 2.0
- Removed "legitimate interest" for Purpose 1 — consent only
- Must show **names and count of vendors** seeking consent
- Improved transparency about data processing
- Removed "out-of-band" consent (all consent must go through CMP)
- Added data categories that must be disclosed (e.g., precise geolocation)

## Technical Components

### TC String (Transparency and Consent String)
Base64-encoded string capturing:
- Which purposes the user consented to
- Which vendors the user consented to
- Whether legitimate interest applies
- The CMP ID
- Timestamp of consent

Stored in the `euconsent-v2` cookie (or `IABTCF_TCString` in localStorage for apps).

### CMP API (`__tcfapi`)
JavaScript API exposed on the page at `window.__tcfapi`. Key commands:
- `__tcfapi('getTCData', 2, callback)` — get current consent data
- `__tcfapi('addEventListener', 2, callback)` — listen for consent changes
- `__tcfapi('ping', 2, callback)` — check if CMP is loaded

The API must be available before ad scripts load. A stub/loader must be present to queue calls.

### Global Vendor List (GVL)
Machine-readable list of registered vendors with their declared purposes. Only vendors on the GVL can use TCF.

## Relationship to GDPR

- TCF is not a legal safe harbor — using a TCF CMP does not guarantee GDPR compliance
- IAB Europe was found to be a joint controller by the Belgian DPA (APD) in 2022
- Many publishers use TCF because ad exchanges (Google Ad Manager, etc.) require it for EU ad serving

### Google Consent Mode v2
Separate from TCF but related. Requires consent signals for:
- `ad_storage`
- `analytics_storage`
- `ad_user_data`
- `ad_personalization`

Became mandatory for Google Ads/GA4 in the EEA in March 2024.

## QA Testing Approach

### Checks to Perform
1. **`__tcfapi` presence**: `window.__tcfapi !== undefined`
2. **TC String validity**: Retrieve and parse the TC string
3. **Consent state before interaction**: `getTCData` should show no consent initially
4. **Consent state after accept**: TC string reflects full consent
5. **Consent state after reject**: TC string reflects no consent for non-essential purposes
6. **Vendor count disclosure**: CMP shows how many vendors request consent
7. **`euconsent-v2` cookie**: Present and matches API response
8. **CMP ID registered**: Check against IAB's CMP list

### Playwright Code Example
```python
tc_data = await page.evaluate("""
    () => new Promise((resolve) => {
        if (typeof __tcfapi !== 'undefined') {
            __tcfapi('getTCData', 2, (data, success) => {
                resolve({available: true, success, data});
            });
        } else {
            resolve({available: false});
        }
    })
""")
```

## Key Sources
- IAB TCF v2.2 Policies: https://iabeurope.eu/tcf-2-0/
- IAB CMP List: https://iabeurope.eu/cmp-list/
- Global Vendor List: https://vendor-list.consensu.org/
