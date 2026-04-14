---
title: Global Privacy Control (GPC)
type: source
tags: [gpc, cookies, consent, us, ccpa, cpra, automation]
date_added: 2026-04-13
authority: GPC Specification / California AG / CPPA
---

# Global Privacy Control (GPC)

## What It Is

GPC is a **browser-level or extension-level signal** that communicates a user's privacy preferences to websites. It is a standardized mechanism for users to express their intent to opt out of the sale/sharing of their personal information.

## Technical Implementation

### HTTP Header
```
Sec-GPC: 1
```

### JavaScript API
```javascript
navigator.globalPrivacyControl === true
```

When present and set to `1`/`true`, GPC signals the user's intent to opt out of the sale/sharing of their personal information.

## Legal Status by Jurisdiction

### Legally Binding
| Jurisdiction | Law | Mandatory From |
|-------------|-----|----------------|
| California | CCPA/CPRA (Section 7025) | Immediately (confirmed by CPPA regulations) |
| Colorado | CPA | July 1, 2024 |
| Connecticut | CTDPA | January 1, 2025 |
| Texas | TDPSA | January 1, 2025 |
| Oregon | OCPA | July 1, 2024 |
| Montana | MTCDPA | October 1, 2024 |

### Not Legally Binding
| Jurisdiction | Law |
|-------------|-----|
| Virginia | VCDPA |
| Utah | UCPA |
| EU/GDPR | No specific provision (but may be treated as withdrawal of consent) |

## How Websites Must Handle GPC

When GPC is detected (`Sec-GPC: 1` or `navigator.globalPrivacyControl === true`):

1. **Do not fire third-party advertising/marketing cookies or pixels**
2. **Do not share personal data with third parties** for cross-context behavioral advertising
3. **Treat it as an opt-out of sale/sharing** under CCPA/CPRA
4. The website **may** display a notice confirming the signal was received
5. The website **must not** require additional action from the user to effectuate the opt-out
6. The website **may** ask the user to confirm if they want to opt out of sale specifically (for disambiguation), but this must not be a barrier
7. If the website also operates under GDPR, GPC should be treated as a withdrawal of consent

## The Sephora Precedent

California AG v. Sephora ($1.2M fine, August 2022):
- **First enforcement action specifically citing GPC**
- Sephora fined for failing to honor GPC signals as opt-out requests
- Established that GPC is a legally binding opt-out signal under CCPA
- Also cited: failure to disclose selling, failure to process opt-out requests
- Set the precedent for all subsequent GPC enforcement

## QA Testing Protocol

### Playwright Implementation
```python
# Create context with GPC signals
context = await browser.new_context(
    extra_http_headers={"Sec-GPC": "1"}
)
# Also inject the JS property
await page.add_init_script("""
    Object.defineProperty(navigator, 'globalPrivacyControl', {
        get: () => true
    });
""")
```

### What to Verify
1. Send request with GPC header — check if tracking cookies are blocked
2. Set `navigator.globalPrivacyControl` — verify behavior change
3. Compare cookie behavior: GPC on vs. GPC off
4. Verify no marketing/advertising third-party requests when GPC is active
5. Check for confirmation notice (optional but good practice)

## Browser/Extension Support

GPC is supported natively or via extensions in:
- Firefox (built-in setting)
- Brave (enabled by default)
- DuckDuckGo browser/extension
- Privacy Badger extension
- Various other privacy extensions

## Key Sources
- GPC Specification: https://globalprivacycontrol.github.io/gpc-spec/
- CPRA Regulations Section 7025 (opt-out preference signals)
- CA AG v. Sephora press release (August 24, 2022)
