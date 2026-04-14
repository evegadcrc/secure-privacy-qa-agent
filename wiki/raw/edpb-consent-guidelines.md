---
title: EDPB Guidelines 05/2020 on Consent
type: source
tags: [edpb, consent, gdpr, cookies, eu]
date_added: 2026-04-13
authority: European Data Protection Board
document: Guidelines 05/2020, adopted 4 May 2020
---

# EDPB Guidelines 05/2020 on Consent under Regulation 2016/679

The definitive interpretation of consent for GDPR compliance. These guidelines are binding guidance from the EDPB.

## On Scrolling/Continued Browsing as Consent (Paragraph 86)

Actions such as scrolling or swiping through a webpage or similar user activity **do NOT satisfy the requirement of a clear and affirmative action**. Such actions "may be difficult to distinguish from other activity or interaction by the user and therefore cannot be regarded as a clear affirmative action."

**Impact on testing:** Any cookie banner that treats continued browsing as consent is non-compliant.

## On Cookie Walls (Paragraphs 38-41)

- Access to services and functionalities must not be made conditional on consent (cookie wall), where such processing is not necessary for the service
- Cookie walls are **not per se prohibited** but are **presumptively invalid**
- A cookie wall makes consent non-free in most cases
- The controller must demonstrate a genuine equivalent alternative (e.g., a paid ad-free version may be acceptable in some member states — this remains debated)

**Impact on testing:** Detect if site content is blocked/hidden behind the consent banner. If refusing cookies makes the site inaccessible, flag as potential cookie wall violation.

## On Pre-ticked Boxes (Paragraph 81)

Pre-ticked opt-in boxes do NOT constitute valid consent. This was definitively confirmed by the Planet49 ruling (CJEU C-673/17).

**Impact on testing:** In any cookie preferences/settings panel, all non-essential categories must default to OFF.

## On Bundled Consent (Paragraphs 42-46)

- Consent must be granular
- Separate consent must be obtained for each distinct purpose
- A single "I accept all" without granular options at the same layer is problematic
- Users must be able to consent separately to different processing operations

**Impact on testing:** The cookie banner must provide category-level controls. "All or nothing" consent is insufficient.

## On Withdrawal of Consent (Paragraphs 113-118)

- Withdrawal must be as easy as giving consent
- If consent is given with one click, withdrawal should also be achievable with comparable ease (no more than the same number of clicks/interactions)
- Technical mechanisms: a clearly visible link/icon to manage cookie preferences at all times, not buried in footer links or privacy policy documents

**Impact on testing:** After giving consent, verify a persistent re-access mechanism exists. Count clicks for withdrawal vs. giving consent — must be comparable.

## On Proof of Consent (Paragraphs 107-112)

Controllers must maintain records that show:
- What information was presented (the banner text/version)
- When consent was given
- Who gave consent (pseudonymous identifier acceptable)
- What they consented to (which categories)
- How consent was collected (mechanism)

Recommended: store a consent receipt (timestamp, version of consent text, choices made, IP hash or similar identifier).

**Impact on testing:** After consent is given, check for a consent cookie that encodes the specific categories consented to, not just a binary yes/no.

## On Freely Given Consent

- If the data subject has no genuine or free choice, consent is not freely given
- Consent tied to contract performance where processing is not necessary = not valid
- Power imbalances (employer/employee, public authority/citizen) make consent presumptively invalid

## Key Source
- EDPB Guidelines 05/2020 — https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en
