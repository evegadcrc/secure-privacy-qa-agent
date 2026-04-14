---
title: Cookie Consent Compliance Wiki — Overview
type: synthesis
tags: [overview, cookies, consent, compliance]
sources: []
created: 2026-04-13
updated: 2026-04-13
---

# Cookie Consent Compliance Wiki

A structured knowledge base covering cookie consent regulations, enforcement, testing methodology, and CMP analysis. Maintained by LLM, curated by humans.

## Start Here

### What Are We Testing?
Our QA agent audits websites for cookie consent compliance. The [[compliance-audit-checklist]] defines every check we perform, from critical legal requirements to best-practice improvements.

### The Two Models
The world splits into [[opt-in-vs-opt-out]]:
- **Opt-in** ([[gdpr]] + [[eprivacy-directive]]): no cookies before consent. Most of the world is adopting this.
- **Opt-out** ([[ccpa-cpra]]): tracking by default, user can refuse. US approach.

See [[global-law-comparison]] for all 18+ jurisdictions.

### What Gets People Fined
The [[enforcement-landscape]] shows that **pre-consent cookies** and **asymmetric reject/accept UI** draw the largest fines. [[cnil]] has fined Google 150M EUR and Facebook 60M EUR for these issues. In the US, failing to honor [[global-privacy-control|GPC]] cost Sephora $1.2M.

## Key Concepts

| Concept | What It Is |
|---------|-----------|
| [[prior-consent]] | No tracking cookies before user says "yes" — the #1 compliance test |
| [[dark-patterns]] | Deceptive UI that manipulates users toward consent — 6 categories per [[edpb]] |
| [[cookie-categories]] | The 5 standard categories from strictly necessary to marketing |
| [[strictly-necessary-cookies]] | The only cookies exempt from consent |
| [[consent-withdrawal]] | Right to change your mind — must be as easy as consenting |
| [[cookie-walls]] | Blocking content until cookies accepted — generally prohibited |

## Regulations & Enforcers

| Entity | Role |
|--------|------|
| [[gdpr]] | EU's data protection regulation — defines "consent" |
| [[eprivacy-directive]] | EU's cookie-specific law — requires consent for device access |
| [[ccpa-cpra]] | California's privacy law — opt-out model with GPC |
| [[lgpd]] | Brazil — GDPR-inspired but no cookie-specific directive |
| [[edpb]] | EU body that issues binding consent & dark pattern guidelines |
| [[cnil]] | France's DPA — largest cookie fines in history |
| [[ico]] | UK's DPA — enforces PECR + UK GDPR |
| [[planet49]] | CJEU ruling that killed pre-ticked checkboxes |
| [[coppa]] | US children's privacy — restricts tracking on kids' sites |

## Technical

| Page | What It Covers |
|------|---------------|
| [[testing-architecture]] | 5-layer testing approach, protocols, iframe handling, code examples |
| [[compliance-audit-checklist]] | Full checklist: 5 critical + 10 major + 8 minor checks |
| [[secure-privacy]] | The CMP we're auditing — iframe architecture, findings, limitations |
| [[iab-tcf]] | IAB TCF 2.2 — the ad industry's consent framework |
| [[global-privacy-control]] | GPC — the browser signal that's legally binding in 6+ US states |

## Wiki Structure

- `raw/` — 22 immutable source documents from deep research
- `pages/` — 24 interlinked wiki pages (entities, concepts, comparisons, syntheses)
- `CLAUDE.md` — schema and conventions
- `index.md` — complete content index
- `log.md` — chronological activity record
