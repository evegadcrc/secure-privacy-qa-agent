---
title: Testing Architecture
type: synthesis
tags: [testing, automation, playwright, cookies]
sources: [raw/automated-testing-methodology.md, raw/secure-privacy-cmp.md, raw/accessibility-requirements.md]
created: 2026-04-13
updated: 2026-04-13
---

# Testing Architecture

How our QA agent implements the [[compliance-audit-checklist]] — the 5-layer architecture, protocols, and technical approaches.

## 5-Layer Architecture

```
Layer 1: Static Analysis ───── DOM/CSS inspection
Layer 2: Dynamic Testing ───── Playwright interaction flows
Layer 3: Cookie & Network ──── Cookie capture + request monitoring
Layer 4: Accessibility ─────── axe-core + keyboard/ARIA checks
Layer 5: AI Analysis ──────── Claude API for language/visual analysis
```

### Layer 1: Static Analysis
Parses banner HTML to check:
- ARIA attributes and roles (see [[accessibility-requirements|accessibility]])
- Color contrast ratios
- Button sizing and prominence ([[dark-patterns]])
- Pre-checked toggle state ([[planet49]])
- Reject button presence at first layer
- Privacy policy link

### Layer 2: Dynamic Interaction Testing
Playwright-driven consent flow testing:
- Fresh visit (clean state) → banner appears
- Accept All → banner dismisses, cookies set
- Reject All → banner dismisses, no tracking cookies
- Customize → granular category selection
- Close/dismiss → no consent implied
- [[Consent withdrawal]] → find settings, change, verify

### Layer 3: Cookie & Network Audit
The [[prior-consent]] protocol:
1. Clean browser profile
2. Navigate to URL
3. Wait 2-3 seconds
4. **Before banner interaction**: capture cookies, network requests, storage
5. Classify cookies against [[cookie-categories|known patterns]]
6. **After each consent action**: re-capture and compare

### Layer 4: Accessibility Audit
WCAG 2.1/2.2 Level AA checks:
- Keyboard navigation (tab order, no traps)
- Screen reader compatibility (ARIA roles, labels, live regions)
- Color contrast (4.5:1 text, 3:1 non-text)
- Focus management (visible indicator, correct movement)
- Text resizing and reflow

### Layer 5: AI Analysis
Claude API for non-automatable checks:
- Banner text clarity and manipulation detection
- Visual design asymmetry assessment
- Compliance scoring
- Report generation with recommendations

## Handling Iframe-Based CMPs

[[Secure Privacy]] and other CMPs render banners in iframes. Standard DOM selectors fail.

### Detection
```python
IFRAME_SELECTORS = [
    '#ifrmCookieBanner',           # Secure Privacy
    '.sp-message-container iframe', # SourcePoint
    '[id*="cookie" i] iframe',
    '[id*="consent" i] iframe',
]
```

### Interaction
```python
# Use frame_locator() — NOT page.locator()
frame = page.frame_locator('#ifrmCookieBanner')
await frame.locator('button').first.wait_for(state='visible', timeout=10000)
text = await frame.locator('body').inner_text()
await frame.locator('button:has-text("Decline")').click()
```

### Fallback
```python
for frame in page.frames:
    if 'cookie' in (frame.name or '').lower():
        buttons = await frame.query_selector_all('button')
```

## [[Global Privacy Control|GPC]] Testing Protocol

```python
context = await browser.new_context(
    extra_http_headers={"Sec-GPC": "1"}
)
await page.add_init_script("""
    Object.defineProperty(navigator, 'globalPrivacyControl', {
        get: () => true
    });
""")
# Verify: no marketing cookies, no ad network requests
```

## [[IAB TCF|TCF]] Verification

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

## Consent Flow Test Matrix

| Flow | Clean State | Expected Banner | Expected Cookies |
|------|------------|-----------------|-----------------|
| Fresh visit | Yes | Visible | Only [[strictly-necessary-cookies\|necessary]] |
| Accept All | Yes | Dismisses | All categories |
| Reject All | Yes | Dismisses | Only necessary + consent cookie |
| Partial | Yes | Dismisses | Only selected categories |
| Close | Yes | Dismisses | Only necessary |
| Return (accepted) | No | Hidden | Per prior choice |
| Return (rejected) | No | Hidden | Only necessary |
| Withdrawal | No (accepted) | Pref panel | Tracking removed |
| GPC enabled | Yes + header | Varies | No marketing |

## Common CMP Failure Modes to Watch

1. **Race condition** — scripts fire before CMP blocks (see [[prior-consent]])
2. **Tag manager bypass** — GTM scripts evade CMP
3. **Iframe leakage** — third-party iframes set cookies independently
4. **Server-side cookies** — `Set-Cookie` headers bypass client-side CMP
5. **Consent desync** — consent cookie expires but tracking cookies remain

See [[secure-privacy]] for specific findings.

## See Also

- [[compliance-audit-checklist]] — what to test
- [[prior-consent]] — the most critical protocol
- [[dark-patterns]] — automated detection methods
- [[cookie-categories]] — classification patterns
- [[secure-privacy]] — iframe-specific challenges
