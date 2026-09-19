# Issue-First Wireframe Contract

**Purpose:** the first viewport of an issue-analysis / incident / work-item system must answer
the issue before it asks the user to explore the system.

Machine profile: `ux_attention_profile.json`.

This is a research-informed design prior, not a universal law of human attention. Validate the
actual product with usability testing and, where justified, eye tracking or interaction
telemetry.

## 1. Attention budget used for information architecture

Therese Fessenden's 2018 NN/g *Scrolling and Attention* study is widely reported as analyzing
130,000+ eye fixations from 120 participants across varied web tasks. Its aggregate viewing-time
distribution provides a useful vertical-priority prior:

| Vertical band | Observed share of page viewing time | Relative index (Screen 1 = 100) | Design priority |
|---|---:|---:|---|
| Screen 1 | 57% | 100 | Critical |
| Screen 2 | 17% | 30 | High |
| Screen 3 | 7% | 12 | Medium |
| Below Screen 3 | 19% **aggregate long tail** | not comparable per screen | Reference |

Cumulative: first 2 screenfuls ≈ 74%; first 3 ≈ 81%.

**Do not misread the final 19% as 19% for every later screen.** It is the combined remainder.
The research summary also reports that more than 65% of first-screen viewing time was
concentrated in its top half; use that as a reason to put the core issue answer there, not as a
fixed pixel formula.

### Derived attention drop heuristic

- Screen 2 has roughly **70% less observed viewing-time share than Screen 1** (17 vs 57).
- Screen 3 has roughly **59% less than Screen 2** (7 vs 17).
- Screen 3 is roughly **88% below Screen 1** in relative viewing-time share.

These ratios are **design priors**, not guaranteed user probabilities.

## 2. Supporting research constraints

- **Position matters.** Still (2018), *Computers in Human Behavior*, found spatial position,
  color, and text style better predicted early entry points than element size alone.
  DOI: `10.1016/j.chb.2018.03.014`.
- **Clutter disperses early attention.** Khoury et al. (2021), *Ergonomics*, found different and
  more widely spread attention during the first 3 seconds on high-clutter websites.
  DOI: `10.1080/00140139.2021.1927200`.
- **Users form a page gist extremely quickly.** Reinecke et al. (2018) showed above-chance web
  category/layout understanding after a 120 ms fixation.
  DOI: `10.1186/s41235-018-0099-2`.
- **Layout order affects dashboard search.** The 2024 Sensors dashboard eye-tracking study
  found core-chart position/layout order materially affected visual search.
  DOI: `10.3390/s24185966`.

Implication: do not try to rescue a badly prioritized layout by merely making the issue title
larger. Put the right information in the right spatial order and reduce competing salience.

## 3. Non-negotiable first-view answer

A user opening an Issue must be able to answer, **without scrolling**:

1. **What is the issue?** — one-sentence retained difference, not a vague ticket title.
2. **What is its state?** — admitted / unresolved / containment / verification / etc.
3. **How serious is it?** — severity/risk tier and blast radius when known.
4. **Who/what is affected?** — scope and agencies/users/systems.
5. **What is confirmed vs unknown?** — never make uncertainty visually disappear.
6. **What should happen next?** — one primary next action.
7. **Who owns the next move?**
8. **How fresh is this answer?** — last evidence/update time or freshness state.

Call this block the **Issue Capsule**.

## 4. Recommended first viewport

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ Breadcrumb / Work item ID                              Updated / Freshness   │
├─────────────────────────────────────────────────────────────────────────────┤
│ ISSUE — one-sentence retained difference                                   │
│ [STATE]  [RISK]  [AFFECTED SCOPE]                                           │
│                                                                             │
│ Confirmed                                      Unknown                       │
│ • fact 1                                        • unknown 1                  │
│ • fact 2                                        • unknown 2                  │
│                                                                             │
│ NEXT ACTION: concise action                         Owner: role/person        │
│ [ Primary action ]             [Secondary] [Secondary]                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Evidence / impact preview                                                   │
│ Enough content visibly continues below ↓                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### First-screen top half

Highest visual priority:
- issue sentence
- state / risk
- confirmed vs unknown distinction
- next action

### First-screen bottom half

Use for:
- evidence/impact preview
- agency/scope preview
- visible continuation cue

Do **not** use the first viewport primarily for:
- decorative hero images
- branding-only blocks
- generic dashboard KPIs
- large navigation menus
- marketing banners
- charts unrelated to the immediate issue

## 5. Screen-by-screen content architecture

### SCREEN 1 — 57% attention prior — `CRITICAL`

Must answer the Issue Capsule completely.

### SCREEN 2 — +17% — `HIGH`

Place:
- evidence summary
- competing hypotheses + challenge status
- architecture impact summary
- affected agencies/rights constraints
- investigation/test plan

### SCREEN 3 — +7% — `MEDIUM`

Place:
- change design
- migration/compatibility
- security/recovery detail
- test evidence detail
- release strategy

### LONG TAIL — remaining 19% aggregate — `REFERENCE`

Place:
- raw logs
- complete timeline
- full audit trail
- deep architecture/reference docs
- historical versions
- appendices

Progressive disclosure should make deep material reachable without forcing it into Screen 1.

## 6. Mobile contract

Mobile is stricter because the viewport is smaller:

```text
[Issue ID] [State] [Risk]

ISSUE
one sentence, 2–4 lines max

CONFIRMED
short bullets

UNKNOWN
short bullets

NEXT ACTION
[ Primary button ]
Owner · freshness

Evidence preview ↓
```

Rules:
- core issue answer precedes nonessential chrome;
- no horizontal scroll for issue comprehension;
- no nested scroll area for Issue Capsule;
- status cannot rely on color alone;
- keep one primary action; max two secondary actions;
- allow evidence/history to collapse below, not the Issue itself.

## 7. Desktop contract

- Put the Issue Capsule on the logical-start reading path and spatial entry region.
- A side panel may contain history/reference only if it does not compete with the core issue.
- Do not rely on card size alone for hierarchy; use position, text style, whitespace, and
  salience deliberately.
- Avoid equal-weight card grids in the first viewport; they communicate that everything is
  equally important.

## 8. No false floor

People scroll, but the first screen must signal that meaningful content continues. Avoid:
- large full-width bars that look like a page ending;
- excessive empty space at viewport bottom;
- nested in-page scrollbars;
- cards aligned to create an accidental visual stop.

Show a natural continuation: partial next section, clipped preview, or explicit but subtle
continuation cue.

## 9. Performance priority

Because the first viewport determines issue comprehension, prioritize its render path:
- issue text/state/risk/action must not wait for deep logs, charts, or history;
- skeletons may reserve secondary regions, but do not skeleton the entire issue answer if the
  core issue data is already available;
- large images and noncritical charts must not block the Issue Capsule.

## 10. Validation: wireframe does not pass by looking good

Hard fail when:
- issue statement is not visible in first view;
- actionable issue has no visible primary next action;
- unknowns exist but UI visually implies resolution;
- decorative/generic content precedes the issue answer;
- false floor hides evidence/detail below;
- mobile requires horizontal scroll for the core answer.

Measure in usability testing:
- `time_to_identify_issue`
- `time_to_identify_current_status`
- `time_to_identify_next_action`
- `scroll_before_issue_comprehension_rate`
- `wrong_next_action_rate`
- `critical_unknown_missed_rate`
- first fixation/interaction region when eye tracking is justified

**Target principle:** a user should be able to restate the issue, current status, and next action
without scrolling.

## References

- Fessenden, T. (2018). *Scrolling and Attention*. Nielsen Norman Group.
  `https://www.nngroup.com/articles/scrolling-and-attention/`
- Still, J. D. (2018). *Web page visual hierarchy: Examining Faraday's guidelines for entry
  points*. Computers in Human Behavior, 84, 352–359. DOI `10.1016/j.chb.2018.03.014`.
- Khoury et al. (2021). *How do we react to cluttered displays? Evidence from the first seconds
  of visual search in websites*. Ergonomics. DOI `10.1080/00140139.2021.1927200`.
- Reinecke et al. (2018). *Web pages: What can you see in a single fixation?* Cognitive
  Research: Principles and Implications. DOI `10.1186/s41235-018-0099-2`.
- *The Effects of Layout Order on Interface Complexity: An Eye-Tracking Study for Dashboard
  Design* (2024). Sensors, 24(18), 5966. DOI `10.3390/s24185966`.
