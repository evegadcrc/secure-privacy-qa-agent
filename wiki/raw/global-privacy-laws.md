---
title: Global Privacy Laws — Cookie and Consent Requirements
type: source
tags: [global-laws, cookies, consent, popia, pdpa, pipl, appi, pipeda, dpdpa]
date_added: 2026-04-13
authority: Various national legislatures
---

# Global Privacy Laws — Cookie and Consent Requirements

Overview of major privacy laws beyond GDPR, CCPA, and LGPD, with focus on cookie/consent-specific requirements.

## POPIA (South Africa — Protection of Personal Information Act, 2013)

- **Effective:** July 2021
- **Cookie requirements:** Requires "consent" for processing personal information; cookies containing personal data need consent. No standalone cookie regulation like ePrivacy.
- **Consent standard:** Must be "voluntary, specific, and informed." Can be implied in some cases but explicit consent is safer for tracking cookies.
- **CMP needs:** Consent banner with opt-out, especially for marketing cookies. Geo-target for South African visitors.

## PDPA (Thailand — Personal Data Protection Act, B.E. 2562)

- **Effective:** June 2022
- **Cookie requirements:** Closely mirrors GDPR. Requires consent for data processing including cookies that collect personal data. Explicit consent needed for sensitive data.
- **Consent standard:** Freely given, specific, informed, and unambiguous. Explicit opt-in for non-essential cookies.
- **Notable:** Thailand's PDPA is very GDPR-aligned. Cookie consent should follow GDPR-like standards.
- **CMP needs:** Full opt-in banner with prior blocking, similar to EU requirements.

## PIPL (China — Personal Information Protection Law)

- **Effective:** November 2021
- **Cookie requirements:** Requires "separate consent" for processing sensitive personal information, cross-border transfers, and sharing with third parties. Cookies used for tracking/profiling likely require separate consent.
- **Consent standard:** Informed, voluntary. Must provide clear notice of processing purposes, methods, categories, retention periods.
- **Notable complexities:**
  - Data localization requirements
  - Mandatory PIAs for cross-border transfer
  - Strict rules on processing by overseas entities
  - Chinese users behind the Great Firewall may have connectivity issues to external CMP scripts
- **CMP needs:** Simplified Chinese language support, separate consent for cross-border transfers, privacy notice requirements.

## APPI (Japan — Act on Protection of Personal Information)

- **Amended 2022 version effective:** April 2022
- **Cookie requirements:** The 2022 amendments introduced "individually identifiable codes" (includes cookies when combined with other data). "Cookie information" alone is treated as "personal-related information" — a lesser category than "personal information."
- **Consent standard:** For personal information, consent is required for certain uses. For cookies alone (personal-related information), consent is not strictly required for collection, BUT consent IS required when providing personal-related information to third parties who will combine it with personal information.
- **Notable:** Japan's approach is more nuanced than GDPR — cookies are not automatically treated the same as personal data unless linked to an identified individual.
- **CMP needs:** Notice about cookie usage, consent mechanism for third-party data sharing scenarios.

## Privacy Act 1988 (Australia)

- **Status:** Currently being reformed (Privacy Act Review)
- **Cookie requirements:** Does NOT specifically regulate cookies. No ePrivacy equivalent. Existing law covers "personal information" which can include cookie data if it identifies an individual.
- **Australian Privacy Principles (APPs):** Require notification about data collection (APP 5) and consent for use/disclosure beyond primary purpose.
- **Reform:** Attorney General's Privacy Act Review (2023-2025) proposed right to erasure and potentially stricter consent rules, but cookie-specific legislation not enacted.
- **CMP needs:** Privacy notice, opt-out for direct marketing (APP 7). Strict cookie banners not legally required but increasingly used as best practice.

## PIPEDA (Canada)

- **Status:** PIPEDA remains in force; Bill C-27 (CPPA) has faced legislative delays.
- **Cookie requirements:** Requires "meaningful consent" for collection, use, and disclosure of personal information. OPC states IP addresses and device identifiers (including cookies) can constitute personal information.
- **Consent standard:** Can be express or implied depending on sensitivity. For non-sensitive business context, implied consent (continued use after notice) may suffice. For sensitive information or tracking, express consent recommended.
- **Quebec's Law 25:** Stricter — requires express prior consent for cookies collecting personal information, similar to GDPR. Applies to Quebec residents specifically.
- **CMP needs:** Banner with consent mechanism, stronger for Quebec visitors. PIPEDA generally allows implied consent with clear notice.

## DPDPA (India — Digital Personal Data Protection Act, 2023)

- **Enacted:** August 2023 (rules pending as of knowledge cutoff)
- **Cookie requirements:** Requires "notice and consent" for processing digital personal data. A "Data Fiduciary" must give clear notice and obtain consent before processing.
- **Consent standard:** "Free, specific, informed, unconditional, and unambiguous" consent by clear affirmative action. Very GDPR-like language.
- **Notable:** Applies only to digital personal data. Has "significant data fiduciary" concept with enhanced obligations.
- **CMP needs:** Consent banner with clear purpose notice, granular options, easy withdrawal. Implementation rules still being finalized.

## Switzerland — nDSG (New Federal Act on Data Protection)

- **Effective:** September 2023
- **Cookie requirements:** Hybrid approach — information duties are mandatory, consent required for certain processing. More aligned with GDPR than previous Swiss law.
- **CMP needs:** Privacy notice, consent mechanism for tracking cookies.

## New Zealand — Privacy Act 2020

- Similar to Australia but with stronger enforcement mechanisms
- Information Privacy Principles require transparency and purpose limitation
- Cookie-specific regulation is limited

## Summary Matrix

| Jurisdiction | Law | Model | Prior Blocking | Reject Button | CMP Approach |
|-------------|-----|-------|----------------|---------------|-------------|
| South Africa | POPIA | Consent | Recommended | Recommended | Opt-in banner |
| Thailand | PDPA | Opt-in (GDPR-like) | Required | Required | Full GDPR-style |
| China | PIPL | Consent | Required | Separate consent | Full banner + localization |
| Japan | APPI | Notice-based | Not required | Not required | Notice + opt-out for 3rd party |
| Australia | Privacy Act | Notice-based | Not required | Not required | Notice only |
| Canada | PIPEDA | Meaningful consent | Not strictly | Recommended | Banner, stronger for Quebec |
| Canada (Quebec) | Law 25 | Opt-in (GDPR-like) | Required | Required | Full GDPR-style |
| India | DPDPA | Opt-in (GDPR-like) | Required | Required | Full GDPR-style |
| Switzerland | nDSG | Hybrid | Recommended | Recommended | Privacy notice + consent |
