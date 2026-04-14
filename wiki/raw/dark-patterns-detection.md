---
title: Dark Patterns Detection — Taxonomy and Methods
type: source
tags: [dark-patterns, consent, testing, automation, edpb, cnil, ftc]
date_added: 2026-04-13
authority: EDPB 03/2022, CNIL, FTC "Bringing Dark Patterns to Light" (2022)
---

# Dark Patterns Detection — Taxonomy and Methods

## EDPB 6-Category Taxonomy (Guidelines 03/2022)

### 1. Overloading
| Pattern | Description | Automated Detection |
|---------|-------------|-------------------|
| Continuous prompting | Repeatedly asking after decline | Monitor for banner reappearance after rejection |
| Privacy maze | Many clicks to find info/controls | Count navigation steps to reach rejection |

### 2. Skipping
| Pattern | Description | Automated Detection |
|---------|-------------|-------------------|
| Deceptive snugness | Most invasive option pre-selected | Check initial toggle/checkbox state — non-essential must default OFF |
| Look over there | Accept prominent, reject minimized | Compare visual properties of accept vs. reject |

### 3. Stirring
| Pattern | Description | Automated Detection |
|---------|-------------|-------------------|
| Emotional steering | Guilt/fear language for declining | NLP/LLM analysis of banner text |
| Hidden in plain sight | Reject less visually prominent | Compare CSS: font-size, color, background, border, element type |

### 4. Hindering
| Pattern | Description | Automated Detection |
|---------|-------------|-------------------|
| Dead end | Reject leads to error/loop | Test reject path, verify completion |
| Longer than necessary | More clicks to reject than accept | Count and compare click paths |
| Misleading information | "Site won't work without cookies" | LLM analysis of banner text |
| Misleading action | Button doesn't match label | Verify button behavior matches label text |

### 5. Fickle
| Pattern | Description | Automated Detection |
|---------|-------------|-------------------|
| Lacking hierarchy | Confusing category order | Structural analysis of preference panel DOM |
| Decontextualizing | Controls in unexpected locations | Check for standard placement patterns |
| Ambiguous wording | Double negatives, unclear labels | NLP/LLM analysis for ambiguity |

### 6. Left in the Dark
| Pattern | Description | Automated Detection |
|---------|-------------|-------------------|
| Language discontinuity | Banner in different language than site | Compare language of banner vs. page content |
| Conflicting information | Banner contradicts cookie policy | Cross-reference banner text with policy |

## FTC Report: "Bringing Dark Patterns to Light" (September 2022)

The FTC identifies these patterns in consent interfaces:
- **Asymmetric consent flows:** Easy to opt in, difficult to opt out ("roach motel")
- **Interface interference:** Visual manipulation including color, size, placement
- **Forced action:** Requiring consent to access content/services
- **Nagging:** Repeated consent prompts after refusal
- **Trick questions:** Double negatives, confusing toggles
- **Confirmshaming:** "No thanks, I don't care about my privacy"
- **Obstruction:** Multiple screens required to reject

## CNIL-Specific Dark Pattern Rules

CNIL has the strictest enforcement:
- **Symmetric choices:** Refusing must be as easy as accepting. "Refuse All" must exist at the same level as "Accept All"
- **No cookie walls:** Conditioning access on acceptance is generally invalid
- **Continued browsing NOT consent:** Scrolling/navigating away is not affirmative action
- **Banner must persist:** No auto-dismiss before user makes active choice
- **Cookie lifetime limits:** Consent cookies max 13 months; re-prompt max 6 months

## Automated Detection Methods

### Button Asymmetry Detection
```
For accept_button and reject_button:
  Compare: font-size (px)
  Compare: padding (px)
  Compare: width, height (px)
  Compare: background-color contrast ratio
  Compare: element type (button vs. a/span)
  Compare: border (present vs. absent)
  Compare: position (above-fold vs. below-fold)
  
  FAIL if:
    - reject font-size < accept font-size * 0.8
    - reject area (w*h) < accept area * 0.5
    - reject has no background but accept does
    - reject is <a> or <span> but accept is <button>
```

### Click Count Comparison
```
accept_clicks = count steps: banner appears → consent given
reject_clicks = count steps: banner appears → consent rejected

FAIL if reject_clicks > accept_clicks + 1
WARN if reject_clicks > accept_clicks
```

### Pre-checked Toggle Detection
```
In preference/settings panel:
  For each category toggle/checkbox:
    If category != "strictly necessary":
      CRITICAL FAIL if toggle.checked == true (default state)
      CRITICAL FAIL if aria-checked == "true" (default state)
```

### Language Analysis (LLM-Assisted)
- Feed banner text + button labels to LLM
- Check for: confirmshaming, emotional manipulation, urgency, misleading claims
- Check for: double negatives, ambiguous toggle labels
- Check for: "Site won't work" / "Missing out" / "Best experience" framing

### Visual Prominence Scoring
```
Score each button on:
  +3 points: background-color with high contrast
  +2 points: border present
  +2 points: large padding (>10px)
  +1 point: bold font-weight
  +1 point: larger font-size
  
Accept_score vs. Reject_score:
  FAIL if Accept_score > Reject_score + 3
  WARN if Accept_score > Reject_score + 1
```
