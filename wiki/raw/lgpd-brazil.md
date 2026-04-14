---
title: LGPD (Brazil) — Cookie Consent Requirements
type: source
tags: [lgpd, cookies, consent, brazil, global-laws]
date_added: 2026-04-13
authority: Lei Geral de Proteção de Dados (Law 13,709/2018)
---

# LGPD (Brazil) — Cookie Consent Requirements

## Overview

LGPD (Lei Geral de Proteção de Dados) is Brazil's comprehensive data protection law. It closely mirrors GDPR in many aspects but has key differences for cookie consent.

## Consent Definition (Article 5, XII)

> "Free, informed, and unambiguous manifestation by which the data subject agrees to the processing of their personal data for a specific purpose."

Very similar to GDPR's definition.

## Legal Bases for Processing (Article 7)

LGPD provides **10 legal bases** for processing personal data, including:
- Consent
- Legitimate interest
- Contract performance
- Legal obligation
- Several others

Unlike GDPR, LGPD does **not** have a direct equivalent to the ePrivacy Directive, so cookie-specific rules are less prescriptive.

## Key Differences from GDPR for Cookies

### 1. No ePrivacy Equivalent
LGPD does not have a separate directive governing cookie placement specifically. The GDPR's strict "prior consent for non-essential cookies" comes from ePrivacy Article 5(3), not GDPR itself. LGPD treats cookies as general personal data processing.

### 2. Legitimate Interest is Broader
LGPD Article 10 allows legitimate interest as a legal basis. The ANPD (Brazilian DPA) has been somewhat more permissive about analytics cookies under legitimate interest than EU DPAs have been.

### 3. No Explicit Opt-In Requirement for Cookies
Unlike GDPR+ePrivacy, LGPD does not explicitly require prior opt-in consent before placing cookies. However, if cookies process personal data (which tracking cookies do), a valid legal basis is needed.

### 4. ANPD Guidance
The ANPD issued guidance on cookies and similar technologies (in 2024) that:
- Recommends consent for non-essential cookies
- Has been less enforcement-heavy than EU DPAs
- Accepts legitimate interest for some analytics use cases

## Consent Requirements Under LGPD

### Specificity (Article 8, para 4)
Consent must refer to specific purposes. Generic authorizations for processing are void.

### Revocation (Article 8, para 5)
Consent can be revoked at any time. The revocation process must be as easy as giving consent.

### Written Consent (Article 8)
If consent is provided in writing, it must be in a clause that stands out from others in the contract.

### Granularity
Consent must be granular per purpose — bundled consent is invalid.

## CMP Configuration for Brazilian Visitors

- Display a consent banner with opt-out capability for analytics/marketing cookies
- Prior blocking is best practice but not strictly legally mandated for all cookies
- Legitimate interest may be acceptable for first-party analytics
- Consent must be specific and granular per purpose
- Withdrawal mechanism must be available and equally easy
- Geo-targeting should serve a different banner to Brazilian visitors vs. EU visitors

## ANPD Enforcement

The ANPD (Autoridade Nacional de Proteção de Dados) was established in 2020. As of 2025:
- Has issued administrative sanctions and warnings
- Less aggressive on cookie enforcement than EU DPAs
- Growing enforcement capacity
- Focus has been on data breach notifications and general compliance

## Key Sources
- LGPD: Law 13,709/2018
- ANPD: https://www.gov.br/anpd/
