---
title: Global Privacy Control (GPC)
type: entity
tags: [gpc, cookies, consent, us, ccpa, automation]
sources: [raw/global-privacy-control.md, raw/us-enforcement-actions.md]
created: 2026-04-13
updated: 2026-04-13
---

# Global Privacy Control (GPC)

A **browser-level signal** that communicates a user's privacy opt-out preference to websites. Transmitted via HTTP header and JavaScript API.

## Technical Implementation

```
HTTP Header:  Sec-GPC: 1
JavaScript:   navigator.globalPrivacyControl === true
```

## Legal Status

### Legally Binding
| Jurisdiction | From |
|-------------|------|
| California ([[ccpa-cpra\|CCPA/CPRA]]) | Immediately |
| Colorado (CPA) | July 2024 |
| Connecticut (CTDPA) | January 2025 |
| Texas (TDPSA) | January 2025 |
| Oregon (OCPA) | July 2024 |
| Montana (MTCDPA) | October 2024 |

### Not Legally Binding
Virginia (VCDPA), Utah (UCPA), EU/[[gdpr]] (no specific provision)

## The Sephora Precedent

The landmark enforcement case: **California AG v. Sephora** ($1.2M, August 2022). Sephora was fined specifically for failing to honor GPC signals. This established GPC as a legally enforceable opt-out mechanism under [[ccpa-cpra|CCPA]].

See [[enforcement-landscape]] for details.

## What Websites Must Do When GPC Is Detected

1. Do **not** fire marketing/advertising cookies or pixels
2. Do **not** share personal data for behavioral advertising
3. Treat as opt-out of sale/sharing under [[ccpa-cpra|CCPA/CPRA]]
4. Must **not** require additional user action to effectuate
5. If under [[gdpr]], treat as withdrawal of consent

## Testing Protocol

```python
context = await browser.new_context(
    extra_http_headers={"Sec-GPC": "1"}
)
await page.add_init_script("""
    Object.defineProperty(navigator, 'globalPrivacyControl', {
        get: () => true
    });
""")
```

Verify: no marketing cookies, no ad network requests, compare behavior GPC on vs. off.

## Browser Support

Natively or via extensions: Firefox, Brave, DuckDuckGo, Privacy Badger, and others.

## See Also

- [[ccpa-cpra]] — the law that makes GPC legally binding
- [[enforcement-landscape]] — Sephora case details
- [[opt-in-vs-opt-out]] — GPC is the technical mechanism for opt-out
- [[testing-architecture]] — GPC testing protocol
- [[secure-privacy]] — claims GPC detection support
