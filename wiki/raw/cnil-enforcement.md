---
title: CNIL Cookie Guidance and Enforcement Actions
type: source
tags: [cnil, enforcement, cookies, consent, france, eu, dark-patterns]
date_added: 2026-04-13
authority: Commission Nationale de l'Informatique et des Libertes (France)
---

# CNIL Cookie Guidance and Enforcement Actions

CNIL has been the most active DPA globally on cookie consent enforcement. Their guidance and fines have set de facto standards for the entire EU.

## CNIL Cookie Guidelines (Deliberation 2020-091, adopted September 2020)

### Core Requirements
1. **No cookies before consent**: No cookie (except strictly necessary) may be deposited before the user has given consent
2. **Continued browsing is NOT consent**: Scrolling or continuing to browse does not constitute valid consent
3. **Symmetric choices**: Refusing cookies must be **as easy** as accepting them. A "Refuse All" button must exist at the same level as "Accept All"
4. **No cookie walls**: Conditioning access to a site on accepting cookies is generally not valid consent (narrow exceptions)
5. **No pre-ticked boxes**: All non-essential cookie categories must default to off
6. **Banner must persist**: The banner must not auto-dismiss before the user makes an active choice
7. **Withdraw as easy as granting**: A persistent mechanism to change cookie preferences must be available

### Cookie Lifetime Limits
- **Consent cookie**: Should not last more than **13 months**
- **Re-prompt interval**: User choice should be remembered for max **6 months** before re-prompting
- Tracking cookies should have lifetimes proportionate to their stated purpose

### Analytics Exception
CNIL permits first-party analytics cookies **without consent** under strict conditions:
- Limited to aggregate audience measurement
- No cross-site tracking
- Anonymized data (IP anonymization)
- No data sharing with third parties
- Limited retention period
- Applies to tools like Matomo (properly configured) and AT Internet
- **Does NOT apply to Google Analytics** (confirmed by multiple rulings)

## Major Enforcement Actions

### Google LLC & Google Ireland — 150M EUR (December 2021)
- **Violation**: google.fr cookie banner did not offer a way to refuse cookies as simply as to accept them
- **Details**: Users had to click multiple times to refuse all cookies, while accepting was a single click
- **Key principle**: Accept and refuse must require the same number of clicks
- **Impact**: Forced Google to add a "Refuse All" button at the first layer

### Facebook Ireland — 60M EUR (December 2021)
- **Violation**: Same as Google — no equally easy refuse mechanism on facebook.com in France
- **Details**: Only "Accept all" and "Manage preferences" were available at the first layer
- **Key principle**: "Manage preferences" as the only alternative to "Accept All" is NOT sufficient

### Microsoft Ireland — 60M EUR (December 2022)
- **Violation**: Cookies deposited without consent on bing.com, and no equivalent reject mechanism
- **Details**: Advertising cookies were set before users could consent
- **Key principle**: Pre-consent blocking is mandatory; reject must be equally prominent

### TikTok — 5M EUR (December 2022)
- **Violation**: No equally easy refuse mechanism; insufficient information about cookie purposes
- **Details**: The refuse process was more complex than acceptance
- **Key principle**: Information requirements must be met alongside symmetric choice

### Criteo — 40M EUR (June 2023)
- **Violation**: Could not demonstrate valid consent for ad-tracking cookies received from partners
- **Details**: Criteo relied on consent collected by partner websites but could not verify that consent was GDPR-valid
- **Key principle**: Controllers must verify and be able to demonstrate that consent they rely on is valid — "we trust our partners' CMPs" is insufficient

## Enforcement Trends

1. **Asymmetric UI is the primary target**: Most CNIL fines relate to reject being harder than accept
2. **Pre-consent cookies are strictly enforced**: Any tracking before consent = violation
3. **Proof of consent matters**: Criteo was fined for not being able to prove consent validity
4. **Large fines for major companies**: CNIL is willing to impose significant financial penalties
5. **Quick iteration**: After fines, companies typically comply within months

## Key Sources
- CNIL cookie guidelines — https://www.cnil.fr/en/cookies-and-other-trackers
- CNIL enforcement decisions — https://www.cnil.fr/en/sanctions
