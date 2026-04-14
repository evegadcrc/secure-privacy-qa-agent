---
title: Global Privacy Law Comparison
type: comparison
tags: [global-laws, cookies, consent, comparison]
sources: [raw/global-privacy-laws.md, raw/lgpd-brazil.md, raw/us-state-privacy-laws.md]
created: 2026-04-13
updated: 2026-04-13
---

# Global Privacy Law Comparison

Cookie consent requirements across 18+ jurisdictions. The "55+ laws" that CMPs like [[secure-privacy]] claim to support.

## Comprehensive Matrix

| Jurisdiction | Law | Model | Prior Blocking | Reject Button | GPC Required | Enforcement |
|-------------|-----|-------|----------------|---------------|-------------|-------------|
| **EU (27)** | [[gdpr]] + [[eprivacy-directive]] | Opt-in | Required | Required (1st layer) | No | DPAs (fines to 4% turnover) |
| **UK** | UK GDPR + PECR | Opt-in | Required | Required | No | [[ico]] |
| **California** | [[ccpa-cpra]] | Opt-out | No | No (opt-out link) | Yes | AG + CPPA |
| **Colorado** | CPA | Opt-out | No | No | Yes (July 2024) | AG |
| **Connecticut** | CTDPA | Opt-out | No | No | Yes (Jan 2025) | AG |
| **Virginia** | VCDPA | Opt-out | No | No | No | AG |
| **Texas** | TDPSA | Opt-out | No | No | Yes (Jan 2025) | AG |
| **Oregon** | OCPA | Opt-out | No | No | Yes | AG |
| **Utah** | UCPA | Opt-out | No | No | No | AG |
| **Brazil** | [[lgpd]] | Hybrid | Not strictly | Recommended | No | ANPD |
| **South Africa** | POPIA | Consent | Recommended | Recommended | No | Info Regulator |
| **Thailand** | PDPA | Opt-in | Required | Required | No | PDPC |
| **China** | PIPL | Consent | Required | Separate consent | No | CAC |
| **Japan** | APPI | Notice | Not required | Not required | No | PPC |
| **Australia** | Privacy Act | Notice | Not required | Not required | No | OAIC |
| **Canada** | PIPEDA | Meaningful consent | Not strictly | Recommended | No | OPC |
| **Canada (Quebec)** | Law 25 | Opt-in | Required | Required | No | CAI |
| **India** | DPDPA | Opt-in | Required | Required | No | DPB |
| **Switzerland** | nDSG | Hybrid | Recommended | Recommended | No | FDPIC |

## Groupings by Approach

### GDPR-Aligned (Strict Opt-In)
EU, UK, Thailand (PDPA), India (DPDPA), Quebec (Law 25), China (PIPL — with local characteristics)

These require full opt-in consent banners with [[prior-consent|prior blocking]], reject at first layer, and granular [[cookie-categories|category]] consent.

### US Opt-Out
California, Colorado, Virginia, Connecticut, Utah, Texas, Oregon, Montana, and growing number of states

These require opt-out mechanisms (links, [[global-privacy-control|GPC]]) but not prior blocking or consent banners.

### Notice-Based (Least Restrictive)
Japan (APPI), Australia (Privacy Act)

Cookie-specific requirements are minimal. Notice and transparency are primary obligations.

### Hybrid
Brazil ([[lgpd]]), Canada (PIPEDA), Switzerland (nDSG), South Africa (POPIA)

Consent required for personal data processing but no cookie-specific directive. Analytics under legitimate interest may be acceptable.

## Implications for CMP Configuration

A CMP claiming "55+ laws" support must:
1. **Geo-detect** visitor location
2. **Serve jurisdiction-appropriate** banner/notice
3. **Apply correct blocking rules** per jurisdiction
4. **Honor jurisdiction-specific signals** (GPC for US states)
5. **Store consent records** meeting each jurisdiction's proof requirements

## See Also

- [[opt-in-vs-opt-out]] — the two fundamental models compared
- [[gdpr]] — the opt-in standard
- [[ccpa-cpra]] — the opt-out standard
- [[lgpd]] — the hybrid approach
- [[secure-privacy]] — claims 55+ law support
- [[compliance-audit-checklist]] — jurisdiction-aware testing
