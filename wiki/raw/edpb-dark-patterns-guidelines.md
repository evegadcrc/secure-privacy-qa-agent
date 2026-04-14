---
title: EDPB Guidelines 03/2022 on Deceptive Design Patterns
type: source
tags: [edpb, dark-patterns, consent, gdpr, eu]
date_added: 2026-04-13
authority: European Data Protection Board
document: Guidelines 03/2022, adopted 14 March 2022, final version February 2023
---

# EDPB Guidelines 03/2022 on Deceptive Design Patterns

Originally targeted at social media platform interfaces, these guidelines are broadly applicable to cookie consent banners and any data protection interface.

## Category 1: Overloading

Bombarding users with requests, information, or options to nudge them toward sharing more data.

### Continuous Prompting
- Repeatedly asking users to accept cookies after they have declined
- Banner reappearing after legitimate rejection
- **Detection:** Monitor for banner re-display after the user has already rejected

### Privacy Maze
- Making it very hard to find information or controls
- Reject option buried deep in settings
- Multiple screens required to reach the reject action
- **Detection:** Count navigation steps to reach rejection vs. acceptance

## Category 2: Skipping

Designing interfaces so that users forget or don't think about data protection.

### Deceptive Snugness
- Designing the interface so the most privacy-invasive option is pre-selected/default
- Pre-ticked category checkboxes in cookie banners
- Non-essential cookies toggled ON by default
- **Detection:** Check initial state of toggles/checkboxes. All non-essential must default to OFF.

### Look Over There
- Drawing attention to a prominent "Accept All" button while the reject option is visually minimized
- **Detection:** Compare visual properties of accept vs. reject elements

## Category 3: Stirring

Appealing to emotions or using visual nudges.

### Emotional Steering
- Language designed to make users feel guilty or fearful for declining
- "You'll miss out on a personalized experience!"
- "We're sad to see you go"
- Confirmshaming ("No thanks, I don't care about my experience")
- **Detection:** NLP/LLM analysis of banner text and button labels

### Hidden in Plain Sight
- Making the reject option visually less prominent
- Smaller font, grey text, no button border vs. bright accept button
- Reject as a text link, accept as a styled button
- **Detection:** Compare CSS properties (font-size, color, background, border, element type)

## Category 4: Hindering

Making it difficult or impossible to exercise data rights.

### Dead End
- Reject option leads to a broken path, error, or loops back
- **Detection:** Test reject path and verify it completes successfully

### Longer Than Necessary
- More clicks required to reject than to accept
- Accept = 1 click; Reject = click "Manage" > uncheck all > click "Save" = 3+ clicks
- **Detection:** Count and compare click paths for accept vs. reject

### Misleading Information
- Suggesting the site won't work without cookies
- "Some features may not be available" when rejecting all cookies
- **Detection:** LLM analysis of banner text for misleading claims

### Misleading Action
- Button labeled in a way that doesn't match its actual function
- "Accept" that actually opens settings rather than accepting
- **Detection:** Verify button behavior matches label

## Category 5: Fickle

Inconsistent or unclear interface design.

### Lacking Hierarchy
- Cookie categories presented in confusing order
- Information structure designed to make it hard to find reject controls
- **Detection:** Structural analysis of preference panel DOM

### Decontextualizing
- Placing consent controls in unexpected locations
- Settings buried in unrelated menus
- **Detection:** Check for standard placement patterns

### Ambiguous Wording
- Double negatives: "Uncheck to not opt out of non-essential cookies"
- Unclear language: toggle says "Enhanced experience" instead of "Marketing cookies"
- **Detection:** NLP/LLM analysis of label text for ambiguity

## Category 6: Left in the Dark

Hiding information, using unclear language, or exploiting uncertainty.

### Language Discontinuity
- Consent banner in a different language than the site
- **Detection:** Compare language of banner text vs. page content

### Conflicting Information
- Banner text contradicts the cookie policy
- Privacy policy says one thing, banner says another
- **Detection:** Cross-reference banner text with linked privacy/cookie policy

## Specific Guidance on Cookie Banners

The EDPB explicitly states:
- Accept and reject must be presented at the **same layer** (first layer of the banner)
- Accept and reject must be given **equal visual prominence** (same size, same color weight, same position level)
- "Manage preferences" as the only alternative to "Accept All" is NOT sufficient — there must be a direct reject option at the first layer
- Pre-selected categories in a preferences panel = dark pattern

## Key Source
- EDPB Guidelines 03/2022 — https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-032022-deceptive-design-patterns-social-media_en
