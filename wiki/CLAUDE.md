# Cookie Consent Compliance Wiki — Schema

This is an LLM-maintained wiki for cookie consent compliance knowledge. The LLM writes and maintains all wiki pages. The human curates sources, asks questions, and guides analysis.

## Directory Structure

```
wiki/
  CLAUDE.md          # This file — schema and conventions
  index.md           # Content index (LLM-maintained)
  log.md             # Chronological activity log (append-only)
  raw/               # Raw source documents (immutable)
  pages/             # Wiki pages (LLM-maintained)
```

## Conventions

### File Naming
- Use kebab-case: `gdpr-consent.md`, `dark-patterns.md`
- Raw sources: `raw/<topic>.md`
- Wiki pages: `pages/<topic>.md`

### Page Format
Every wiki page starts with YAML frontmatter:

```yaml
---
title: Page Title
type: entity | concept | comparison | summary | synthesis
tags: [gdpr, consent, cookies]
sources: [raw/source1.md, raw/source2.md]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Page Types
- **entity**: A specific law, regulation, ruling, organization, or tool (e.g., GDPR, CNIL, Planet49)
- **concept**: An idea or principle (e.g., Prior Consent, Dark Patterns, Cookie Categorization)
- **comparison**: Side-by-side analysis (e.g., GDPR vs CCPA, Opt-In vs Opt-Out models)
- **summary**: Overview of a source document
- **synthesis**: Cross-cutting analysis connecting multiple topics

### Links
Use Obsidian wikilinks: `[[page-name]]` or `[[page-name|display text]]`
For raw sources: `[[raw/source-name]]`

### Cross-References
- Every wiki page should link to related pages
- Every concept should link to the laws that define it
- Every enforcement case should link to the violated principles
- Maintain a "See also" section at the bottom of each page

## Workflows

### Ingest
When processing a new raw source:
1. Read the source completely
2. Create or update relevant wiki pages
3. Update `index.md` with new/changed pages
4. Append to `log.md`
5. Check for contradictions with existing pages

### Query
When answering a question:
1. Read `index.md` to find relevant pages
2. Read the relevant pages
3. Synthesize an answer with `[[wikilinks]]` citations
4. If the answer is valuable, file it as a new wiki page

### Lint
Periodic health check:
1. Find orphan pages (no inbound links)
2. Find contradictions between pages
3. Find stale claims superseded by newer sources
4. Suggest missing pages for important concepts
5. Suggest new sources to investigate

## Tags Vocabulary
`gdpr`, `eprivacy`, `ccpa`, `cpra`, `lgpd`, `coppa`, `tcf`, `gpc`, `cnil`, `ico`, `edpb`, `enforcement`, `dark-patterns`, `accessibility`, `wcag`, `cookies`, `consent`, `cmp`, `secure-privacy`, `testing`, `automation`, `us-state-laws`, `global-laws`
