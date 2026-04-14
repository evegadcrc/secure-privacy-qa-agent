---
title: Dark Patterns in Cookie Consent
type: concept
tags: [dark-patterns, consent, edpb, cnil, ftc, testing]
sources: [raw/edpb-dark-patterns-guidelines.md, raw/dark-patterns-detection.md, raw/cnil-enforcement.md]
created: 2026-04-13
updated: 2026-04-13
---

# Dark Patterns in Cookie Consent

Deceptive design patterns that manipulate users toward consenting to data processing they would otherwise refuse. Prohibited by [[edpb]] Guidelines 03/2022, [[cnil]] enforcement, FTC guidance, and [[ccpa-cpra|CPRA]] statute.

## The EDPB Taxonomy (6 Categories)

### 1. Overloading
- **Continuous prompting** — banner reappears after rejection
- **Privacy maze** — too many clicks to find reject option

### 2. Skipping
- **Deceptive snugness** — non-essential categories pre-toggled ON (violates [[planet49]])
- **Look over there** — accept prominent, reject minimized

### 3. Stirring
- **Emotional steering** — "You'll miss out on a personalized experience!"
- **Hidden in plain sight** — reject as grey text link, accept as bright button

### 4. Hindering
- **Dead end** — reject leads to error or loops
- **Longer than necessary** — accept = 1 click, reject = 3+ clicks
- **Misleading info** — "Site won't work without cookies"

### 5. Fickle
- **Lacking hierarchy** — confusing category layout
- **Ambiguous wording** — double negatives, unclear toggles

### 6. Left in the Dark
- **Conflicting info** — banner contradicts cookie policy
- **Language discontinuity** — banner in different language than site

## Legal Status

| Framework | Status |
|-----------|--------|
| [[edpb]] 03/2022 | Binding guidance for EU DPAs |
| [[cnil]] | Actively enforced (Google 150M EUR, Facebook 60M EUR) |
| [[ccpa-cpra\|CPRA]] Section 1798.140(l) | Statutory definition — consent via dark patterns is void |
| FTC "Bringing Dark Patterns to Light" (2022) | Enforcement under Section 5 |

## The "Symmetric Choice" Principle

[[cnil]]'s core enforcement standard: **refusing cookies must be as easy as accepting them.**

This means:
- "Reject All" button at the **same layer** as "Accept All"
- **Same visual prominence** — size, color, styling
- **Same number of clicks** — if accept is 1 click, reject must be 1 click
- "Manage Preferences" alone is NOT a substitute for a reject button

## Automated Detection

| Pattern | Detection Method |
|---------|-----------------|
| Button asymmetry | Compare CSS: font-size, padding, background-color, dimensions, element type |
| Click count disparity | Count steps for accept vs. reject paths |
| Pre-checked toggles | Check initial state of checkboxes in preferences panel |
| Confirmshaming | LLM analysis of button labels and banner text |
| Missing reject button | DOM check for reject/decline button at first layer |
| Language manipulation | LLM analysis for emotional steering, double negatives |

See [[testing-architecture]] for implementation details.

## See Also

- [[edpb]] — authored the dark patterns taxonomy
- [[cnil]] — most active enforcer
- [[planet49]] — pre-ticked boxes ruling
- [[consent-withdrawal]] — dark patterns also affect withdrawal
- [[compliance-audit-checklist]] — criteria M1, M2, M7
- [[opt-in-vs-opt-out]] — dark patterns exist in both models
