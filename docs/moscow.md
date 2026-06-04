# MoSCoW Prioritisation

Classifying the 21 user stories from [`user-stories.md`](user-stories.md) into Must / Should / Could / Won't for v1, with a one-line justification for each.

The classification reflects a deliberately disciplined scope for the build window available. The principle: a feature is **Must** only if at least one primary persona could not complete their core task without it. Everything else is **Should** at most.

This is not the maximum we *could* build; it is the minimum that demonstrates the concept honestly. Underpromising and overdelivering scores better than the reverse — and it protects the testing, sustainability analysis, and user-testing work that the rubric also weights.

## Summary

| Bucket | Count | What it means |
|---|---|---|
| Must | 7 | The prototype is not the prototype without these. Failure on any of these is a failure of the project. |
| Should | 10 | Strong targets for v1. Promoted to Must only if Must items finish early. |
| Could | 3 | Nice-to-haves that improve the demo if time allows. Cut without regret if not. |
| Won't | 1 | Explicitly out of scope for v1, documented so the decision is visible. |

---

## Must (7)

These are the smallest set of stories such that all three resident personas (Margaret, Aisha, Mahmoud) can complete a meaningful task, and the secondary stakeholder (Sarah) can keep the data current.

| ID | Story (short form) | Why Must |
|---|---|---|
| **US-01** | Find a service without creating an account | Margaret abandons the system if the first thing it asks for is an email. No account = baseline of the design philosophy. |
| **US-03** | Understand what each service is before clicking | Without plain-English descriptions, no persona can decide whether a service is right for them. Failure here means no successful task completion. |
| **US-04** | Find services open right now | Aisha's primary task. The "open now" filter is the single most valuable feature differentiating this from a generic directory. |
| **US-05** | Search by need, not category | Without need-based search, the system requires users to learn its taxonomy — which all three personas explicitly cannot or will not do. |
| **US-06** | Show eligibility (voucher/referral/drop-in) on result cards | Aisha being turned away in front of her kids is the failure mode the system exists to prevent. Eligibility must be visible at the result-card level, not buried. |
| **US-13** | Org admin can add a service | Without this, the system has no data and no path to having data. Sarah must be able to populate the directory. |
| **US-17** | Save confirmation for admin changes | Sarah needs to trust the system, and trust depends on visible feedback that her changes saved. Sounds small; isn't. |

**Total Must = 7 stories.** Built well, these alone demonstrate that the concept works.

---

## Should (10)

Strong targets if Must items complete on schedule. Each of these meaningfully improves the experience for at least one persona, but the system still works without them.

| ID | Story (short form) | Why Should not Must |
|---|---|---|
| **US-02** | Comfortable text size and contrast | Implemented through the base CSS — likely "free" given accessibility-first defaults are already in `style.css`. Promoting to Must depends on whether dedicated time is spent on accessibility audit. |
| **US-07** | Works on slow connections | Server-rendered HTML naturally achieves much of this. Achieving the 3-second target on simulated 3G needs measurement — a Should because measurement and tuning take time. |
| **US-08** | Walking distance instead of driving | High value but requires geocoding + a distance calculation. Likely deliverable, but if the geocoding library proves fiddly, it can be cut to a simpler "in Ladywood / outside Ladywood" boolean for v1. |
| **US-09** | Filter by language spoken | Requires the `languages_spoken` field on the Service model and a filter UI. Achievable, but only delivers value if seed data is populated with real language information (which depends on time). |
| **US-11** | Cultural notes on service entries | A free-text field on the Service model and a section on the detail page — small implementation. Should rather than Must because the value depends on having real cultural notes in the seed data. |
| **US-14** | Quick partial-field updates | The Must implementation of US-13 will already support save-without-re-entering by default if built with a standard form. Promoted to Should rather than Must because targeted testing of the workflow is still required. |
| **US-15** | Login without 2FA | A simple email/password login. Should not Must because login is only needed *if* Sarah's admin flow is fully exercised in the demo; a "logged-in dev user" pre-fill is an acceptable fallback for v1. |
| **US-18** | Works on multiple devices | Inherent to a server-rendered responsive design. Likely a Should that lands without explicit work, but verifying on multiple devices is a separate task that takes time. |
| **US-19** | No third-party tracking | Largely a *decision* rather than a *feature* — implemented by not adding GA, no CDN fonts, etc. Should because the audit step (network inspection) needs doing and documenting. |
| **US-20** | "Last updated" date on service pages | Trivial implementation (a column on the model, a render on the page) but adds real trust. Should rather than Must only because residents can complete their task without it. |

---

## Could (3)

Welcome additions if the Must and Should buckets close cleanly. Worth listing because they make for a stronger demo if delivered, but no time is committed to them.

| ID | Story (short form) | Why Could |
|---|---|---|
| **US-12** | Printable service pages | Mostly a CSS `@media print` ruleset. Small effort, real value for Mahmoud. Could rather than Should because it benefits one persona's edge case. |
| **US-16** | Mark service as temporarily closed | A boolean field + a banner on the detail page + an exclusion from "Open now". Small work, but compounds with the opening-hours model's complexity. |
| **US-21** | Empty-state shows helplines | Static content with two or three verified national helplines. Easy if time allows; replaceable with a simple "Try a different search" message if not. |

---

## Won't (for v1) (1)

Documented so the decision is visible to markers and to a future maintainer.

| ID | Story (short form) | Why Won't |
|---|---|---|
| **US-10** | Full UI translation into Arabic | Translation is more than `gettext`-style string substitution — it requires native-speaker review, RTL layout testing, and ongoing maintenance for every new UI string. Doing it badly is worse than not doing it; doing it well is a v2 project. The system still serves Mahmoud through US-09 (filter by language) and US-11 (cultural notes), and Google Translate handles the rest acceptably for v1. |

---

## Implications for the rest of the project

- **Class diagram (`uml/class-model.png`):** must include every entity touched by a Must story. Concretely: `Service`, `Location`, `OpeningHours`, `EligibilityRule`, `OrgAdmin`. The `Language` entity is Should-driven and can be added if US-09 lands. Cultural-notes and "last updated" fields go directly on `Service` as Should-driven attributes.
- **Test plan:** every Must story must have at least one automated or manual test that verifies its acceptance criteria. The 10% Testing mark depends on this.
- **User testing scenarios:** drawn from Must stories first. Two scripted tasks for external participants — one Margaret-style (US-01, US-03), one Aisha-style (US-04, US-05, US-06) — cover the core flows.
- **Presentation:** the demo walks through the Must stories. Should items are mentioned as "also delivered" if applicable. Could items are bonuses. The Won't decision is explicitly defended.

## Re-prioritisation triggers

The MoSCoW is not frozen. Promote a Should to Must if:

- Must items are complete and tested by end of Day 5.
- A group member joins and contributes capacity.

Demote a Must to Should only if:

- A genuine technical blocker emerges (e.g., a chosen library doesn't work as documented).
- The blocker is documented in the design log with the reason for demotion.

Demotions are recorded as decisions in the docs — they are not silent.
