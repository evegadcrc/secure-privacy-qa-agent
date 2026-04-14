---
title: Secure Privacy CMP — Architecture and Testing Analysis
type: source
tags: [secure-privacy, cmp, cookies, iframe, testing]
date_added: 2026-04-13
authority: Direct audit findings + industry knowledge
---

# Secure Privacy CMP — Architecture and Testing Analysis

## Company Overview

**Secure Privacy** (secureprivacy.ai) is a Consent Management Platform founded in 2019, headquartered in the US. They claim compliance with GDPR, CCPA, LGPD, and 55+ global privacy laws.

## Claimed Features
- Automated cookie scanning, categorization, and consent collection
- Auto-blocking of scripts/cookies until consent is granted
- DSAR (Data Subject Access Request) automation
- Data mapping and processing activity inventory
- Privacy policy and cookie policy generation/hosting
- Consent records/logging with timestamped proof
- Geo-targeting (different banners per visitor jurisdiction)
- IAB TCF 2.2 compliance (verify CMP ID on IAB list)
- Google Consent Mode v2 integration
- GPC (Global Privacy Control) signal detection
- White-label flexibility

## Technical Architecture: Iframe-Based Banner

### How It Works

1. **Script injection:** Website adds `<script src="https://app.secureprivacy.ai/script/<site-id>.js">`
2. **Iframe creation:** Bootstrap script creates `<iframe id="ifrmCookieBanner">` with `srcdoc`
3. **Banner rendering:** All UI (text, buttons: Accept all, Decline, Customize) renders inside the iframe
4. **Script blocking:** Uses script-rewriting — changes `type` from `text/javascript` to `text/plain` or custom type (e.g., `text/sp-javascript`), preventing browser execution. On consent, type is changed back and scripts re-execute. May use MutationObserver to intercept dynamically added scripts.
5. **Cookie categorization:** Automated scan categorizes cookies (necessary, analytics, marketing, preferences). Manual override available.
6. **Consent storage:** First-party cookie (often `sp_consent` or similar) and potentially `localStorage`
7. **Cross-domain:** Supports multi-domain consent sharing

### The Iframe Element

```html
<iframe srcdoc="<!DOCTYPE html><html><head><meta name='robots' content='noindex'/></head><body></body></html>" 
  title="Cookie Banner" 
  id="ifrmCookieBanner" 
  role="application" 
  tabindex="0" 
  aria-label="Cookie Banner" 
  style="border: none; height: 125px;">
</iframe>
```

**Key observations:**
- `srcdoc` iframe = technically same-origin with parent page
- Empty `<body>` suggests content injected asynchronously
- `role="application"` and `aria-label` provide some accessibility hooks
- `tabindex="0"` makes the iframe focusable

## Audit Findings (from our QA agent)

### Pre-Consent Cookie Leakage (CRITICAL)
Our audit found `_gcl_au` (Google Ads) and `test_cookie` (DoubleClick) loading BEFORE consent on secureprivacy.ai itself. Root causes:
- Google Ads/Analytics scripts loaded via tag manager or directly in HTML before CMP's blocking script intercepts
- Script execution order: tracking scripts in HTML before CMP script
- Auto-blocking may not cover all script loading methods (inline, pixel images, script-loaded scripts)

### Iframe Testing Limitation (MAJOR)
Could not verify post-rejection behavior because iframe prevented automated button interaction.

## Iframe Testing Challenges

### DOM Isolation
Standard CSS selectors from parent page cannot reach iframe content. `document.querySelector('#ifrmCookieBanner button')` WILL NOT WORK.

### Cross-Origin Restrictions
If iframe is cross-origin, `contentDocument` is inaccessible (SecurityError). Secure Privacy's `srcdoc` is same-origin, but content may be populated by scripts from secureprivacy.ai domain.

### Playwright Solutions

**Using frame_locator() (recommended):**
```python
frame = page.frame_locator('#ifrmCookieBanner')
await frame.locator('button:has-text("Accept")').click()
```

**Waiting for async content:**
```python
await page.wait_for_selector('#ifrmCookieBanner', state='attached')
frame = page.frame_locator('#ifrmCookieBanner')
await frame.locator('button').first.wait_for(state='visible', timeout=10000)
```

**Extracting text and buttons:**
```python
frame = page.frame_locator('#ifrmCookieBanner')
text = await frame.locator('body').inner_text()
buttons = await frame.locator('button').all_inner_texts()
```

**Fallback via page.frames:**
```python
for frame in page.frames:
    if 'cookie' in (frame.name or '').lower() or 'consent' in (frame.url or '').lower():
        buttons = await frame.query_selector_all('button')
```

### Known Iframe CMP Selectors
```python
IFRAME_SELECTORS = [
    '#ifrmCookieBanner',           # Secure Privacy
    '#sp-cc iframe',               # Secure Privacy variant
    '[id*="cookie" i] iframe',
    '[id*="consent" i] iframe',
    '.cmp-container iframe',
    '#cmpbox iframe',
    '.sp-message-container iframe', # SourcePoint
]
```

## Impact on QA Agent Architecture

The current `banner_detector.py` uses `page.locator(selector)` which only searches parent DOM. For iframe-based CMPs:

1. First try parent DOM selectors (current approach)
2. If iframe detected but no buttons: switch to `frame_locator()`
3. Extract buttons and text from within iframe context
4. In `flow_tester.py`: use `frame_locator()` to click buttons
5. Wait for async content loading inside iframe

This is the root cause of why the audit detected the banner's presence but couldn't extract text/buttons or test consent flows.
