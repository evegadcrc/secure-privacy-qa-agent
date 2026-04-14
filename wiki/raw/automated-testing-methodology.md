---
title: Automated Cookie Consent Testing Methodology
type: source
tags: [testing, automation, cookies, consent, playwright]
date_added: 2026-04-13
authority: Industry best practices, tool ecosystem analysis
---

# Automated Cookie Consent Testing Methodology

## 5-Layer Testing Architecture

### Layer 1: Static Analysis (DOM/CSS)
- Parse banner HTML structure
- Check ARIA attributes, roles, labels
- Evaluate color contrast, button sizing
- Detect pre-checked toggles
- Check for reject button presence at first layer
- Verify privacy policy link

### Layer 2: Dynamic Interaction Testing (Playwright)
- Simulate fresh visit (clear all cookies/storage)
- Detect and interact with consent banner (including iframe-based)
- Test all consent paths: accept, reject, customize, close
- Compare cookies before/after each action
- Test consent withdrawal flow
- Measure click counts per path

### Layer 3: Cookie & Network Audit
- Inventory all cookies (name, domain, path, expiry, secure, httpOnly, sameSite)
- Compare against CMP declarations
- Categorize using known cookie databases
- Flag undeclared cookies
- Monitor network requests to tracking domains
- Check localStorage/sessionStorage for tracking data

### Layer 4: Accessibility Audit
- WCAG compliance of banner HTML (axe-core)
- Keyboard navigation testing
- Screen reader attribute verification
- Focus management verification
- Responsive/zoom testing

### Layer 5: AI-Powered Analysis (Claude API)
- NLP analysis of banner text for clarity/dark patterns
- Visual analysis of banner design for asymmetries
- Compliance scoring against regulatory checklists
- Report generation with findings and remediation

## Pre-Consent Cookie Capture Protocol

This is the **most critical test.** Exact sequence matters:

1. Launch browser with **clean profile** (no cookies, no storage, no cache)
2. Set standard user-agent string
3. Navigate to target URL with `wait_until="domcontentloaded"`
4. Wait 2-3 seconds for delayed scripts/CMPs to load
5. **Before ANY banner interaction**, capture:
   - All browser cookies (`context.cookies()`)
   - All localStorage entries
   - All sessionStorage entries
   - Network request log (tracking domain calls)
6. Classify every captured cookie
7. Any non-necessary cookie = **CRITICAL violation**

## Post-Consent Cookie Capture Protocol

After each consent action:
1. Perform consent action (click button)
2. Wait 2-3 seconds for scripts to execute and cookies to settle
3. Capture all cookies, storage, and network requests
4. Compare against pre-consent state
5. Validate against expected outcome per flow type

## GPC Testing Protocol

```python
# Create context with GPC signals
context = await browser.new_context(
    extra_http_headers={"Sec-GPC": "1"}
)
await page.add_init_script("""
    Object.defineProperty(navigator, 'globalPrivacyControl', {
        get: () => true
    });
""")
# Navigate and verify: no marketing cookies, no ad network requests
```

## TCF Verification Protocol

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

Check:
- `__tcfapi` present
- TC string parseable
- Consent state matches user choices
- `euconsent-v2` cookie matches API response

## Consent Flow Test Matrix

| Flow | Clean State | Action | Banner Expected | Cookie Expected |
|------|------------|--------|-----------------|-----------------|
| Fresh visit | Yes | None | Visible | Only necessary |
| Accept All | Yes | Click "Accept" | Dismisses | All categories may appear |
| Reject All | Yes | Click "Reject" | Dismisses | Only necessary + consent cookie |
| Partial consent | Yes | Manage > select some > save | Dismisses | Only selected categories |
| Close/dismiss | Yes | Click X | Dismisses | Only necessary (no consent given) |
| Return (accepted) | No (has consent cookie) | Navigate | Hidden | Per prior choice |
| Return (rejected) | No (has consent cookie) | Navigate | Hidden | Only necessary |
| Withdrawal | No (accepted state) | Find settings > change > save | Pref panel opens | Tracking cookies removed |
| GPC enabled | Yes + GPC header | Navigate | May vary | No marketing cookies |

## Existing Tools and Ecosystem

| Tool | Type | Strengths | Limitations |
|------|------|-----------|-------------|
| Cookiebot Scanner | SaaS | Auto-categorization | Misses dynamic/SPA cookies |
| Privado | SaaS/CLI | Code-level data flow analysis | Not runtime behavior |
| 2GDPR | SaaS | Quick scanning | Limited consent flow testing |
| CookieMetrix | SaaS | User interaction simulation | Limited dark pattern detection |
| axe-core | Library | WCAG compliance | No cookie-specific context |
| Playwright | Framework | Full browser automation | Requires custom scripts |
| Lighthouse | Tool | Performance + accessibility | General, not cookie-specific |

## What CAN Be Automated

- Cookie inventory (before/after consent)
- Prior blocking verification
- Consent flow click-through
- Banner presence detection
- Accessibility checks (ARIA, contrast, keyboard)
- Button presence and basic styling comparison
- Pre-ticked checkbox detection
- Click count comparison
- Consent persistence across sessions
- GPC signal testing
- TCF API validation
- Network request monitoring
- Cookie attribute checks (Secure, HttpOnly, SameSite)

## What CANNOT Be Fully Automated

| Area | Why | Approach |
|------|-----|----------|
| Legal accuracy of descriptions | Requires legal judgment | Flag for manual review |
| "Strictly necessary" legitimacy | Legal question | Flag suspicious cookies |
| Language clarity sufficiency | Nuance in legal adequacy | LLM analysis + manual review |
| Emotional manipulation | Contextual understanding needed | LLM analysis + manual review |
| Privacy policy consistency | Full document cross-reference | LLM-assisted comparison |
| Jurisdictional applicability | Legal analysis required | Geo-detection + configurable rules |
| Data sharing chains | Full recipient chain | Network analysis + manual investigation |

## Key Technical Considerations

- **Race conditions:** Cookies set asynchronously; wait for network idle after consent
- **Iframes:** Many CMPs render in iframes; use `frame_locator()` for cross-iframe access
- **Shadow DOM:** Some CMPs use Shadow DOM; ensure selectors can pierce it
- **Service workers:** May cache cookies or interfere with consent
- **SPA navigation:** Behavior may differ on client-side vs. full page loads
- **Geographic variation:** CMP behavior varies by detected location; test from multiple geos
- **A/B testing:** Some sites A/B test banners; results may vary between runs
- **Dynamic script loading:** Scripts loaded via document.write, eval, dynamic imports, Web Workers may evade CMP blocking
