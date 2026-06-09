# User Testing Results

Findings from external user testing of the Ladywood Community Services
Finder prototype. The plan that was followed is in
[`user-testing-plan.md`](user-testing-plan.md).

## Summary

Two participants ran through three persona-aligned scenarios each. Both
completed all scenarios including, eventually, the older participant
who is the persona most at risk of being designed around. Three usability
findings emerged that the writeup acts on. One is significant enough
that it changes the prioritisation of v1.1 work.

| | P1 (Margaret-aligned) | P2 (convenience, also Aisha-aligned in part) |
|---|---|---|
| **Age** | 60s | 16 |
| **Tech confidence** | Low–medium | High |
| **Relation** | Mother | Sister |
| **Scenario 1 (food bank, no account)** | Completed with hesitation | Completed |
| **Scenario 2 (open now, urgent)** | Completed (but did not notice the filter) | Completed (did not notice the filter) |
| **Scenario 3 (English classes)** | Completed | Completed |

n=2 is below the conventional usability research minimum of 5. The
findings here are treated as case studies, not a sample. The brief
explicitly forbids contacting actual Ladywood residents; the choice of
participants reflects that constraint.

---

## What worked

### No-account access is genuinely invisible to users (US-01 confirmed)

Neither participant remarked on the absence of a signup wall. Neither
expected one. For Margaret-aligned P1, this is exactly the desired
behaviour, the design implication from her persona ("the system has to
be useful in the first 10 seconds or she closes it") was met. Both
participants began searching within seconds of the homepage loading.

### Plain-English descriptions worked, even for the older participant

P1 did not ask "what does this mean?" at any point during the scenarios.
The 280-character limit on descriptions and the deliberately plain
register appear to have done their job. Both participants understood
service summaries on first read.

### Service detail pages are doing their job

Both participants clicked into at least one service detail page (rather
than basing their final answer purely on the result card). This was
explicitly the design intent, result cards give a fast overview, detail
pages give the trustworthy specifics. P1 in particular used the detail
page's opening hours table to find the closing time in Scenario 2.

---

## What did not work

### The category tiles were invisible to both participants

Neither participant tapped a category tile on the homepage. Both typed
into the search box instead. This is a significant finding — the tiles
were designed specifically for Margaret-aligned users on the assumption
that tapping is easier than typing. The data does not support that
assumption.

P1 (the persona-aligned participant) confirmed afterward that she had
not realised the tiles were tappable buttons; she had read them as
example text or decoration.

**Implication for v1.1:** the category section needs visual treatment
that signals interactivity more clearly. Possibilities: button styling
with a clear background/border, slight elevation, a hint like "Tap a
category to see services."

### The "open now" toggle was invisible to both participants

Neither participant noticed the "Only show places open right now"
checkbox at the top of the homepage's search form. Both completed
Scenario 2 (which asked for somewhere "open right now") by typing
"food" and looking at the "Open now" labels on individual result
cards rather than by using the dedicated filter.

This is a serious finding because the open-now filter is the single
most valuable feature for Aisha's persona, and it was effectively
absent from both participants' experience. The filter is doing real
work (it is on by default, and Aisha-aligned users get filtered
results without realising), but its discoverability is poor.

**Implication for v1.1:** the open-now filter needs either visual
prominence (button-style toggle rather than a checkbox tucked under
the search box) or removal as a default with a clearer affordance.

This is the most significant finding from the testing.

### P1 took noticeably longer than P2 on Scenario 2

While both participants completed all three scenarios, P1 (the older,
less digitally confident participant) took meaningfully longer on
Scenario 2, the time-sensitive one Aisha would attempt. She got
there, but with hesitation between steps. This suggests the resident
flow may need a more obvious "I need help right now" prompt for users
who are not used to refining searches.

**Implication for v1.1:** consider a "Quick links" row on the homepage
for the most time-sensitive needs (food banks, warm spaces) — single-tap
journeys for users with low confidence and high urgency.

---

## Limitations

This study has known constraints. The writeup is honest about them
rather than treating them as edge cases:

1. **n=2 is below conventional usability minimums.** Three (Nielsen's
   classic 80% rule for catching issues) was the target; recruiting
   was difficult inside the brief's constraint of no direct contact
   with Ladywood residents.

2. **No participant aligned with the Mahmoud persona.** Recent migrants
   with limited English were not reachable inside the timeline. The
   ESOL scenario was substituted in the test plan as something v1
   actually supports, but a Mahmoud-aligned participant would
   plausibly find more issues than P1 or P2 did.

3. **The observer was the project author**, which introduces an
   experimenter-bias risk: participants may have understated confusion
   or unconsciously performed for the observer. Both participants are
   family members, which may amplify this further.

4. **Note-taking during sessions was inconsistent**, particularly in
   the first session. The findings reported here are a combination of
   contemporaneous notes (P2) and post-session recall with the
   participant present for confirmation (P1). The writeup specifically
   distinguishes high-confidence claims from recall-only claims where
   relevant.

5. **The seed data has known gaps** (`needs_verification: true` on
   7 of 13 services). Participants encountered this, for example,
   in Scenario 3 the ESOL services had "contact to enrol" notes
   rather than specific class times, but both still found what they
   were looking for.

6. **Both participants are personally known to the researcher.**
   Strangers would likely have produced richer "thinking aloud" data.

---

## What this would change in v1.1

In priority order, the three concrete UI changes I would prioritise
next based on these findings:

1. **Make the "open now" filter visible.** Either as a prominent
   toggle button (not a checkbox) at the top of the homepage, or by
   reframing the filter as a two-mode entry point ("Open now" vs
   "All services") with the choice obvious from the homepage.

2. **Style the category tiles as obvious buttons** — clear
   background, perhaps icons, and ideally a one-line caption
   ("Tap a category for instant results").

3. **Add a "Quick help" row on the homepage** for the most urgent
   needs, single-tap journeys to food banks open now, warm spaces
   open now, food parcels available today.

A fourth, methodological change: line up at least one Mahmoud-aligned
participant for the next round of testing, recruited via a community
ESOL service rather than personal contacts.

---

## Per-scenario notes

### Scenario 1 — Margaret-style (food bank, no account)

**P1 (Margaret-aligned):** Used the search box, typed "food bank",
read through results, clicked into one detail page to find the
address. Completed in approximately 2 minutes. Comment afterward
(paraphrased from recall): the page felt straightforward and she
didn't feel rushed.

**P2 (convenience):** Used search, completed within 30 seconds, no
hesitation.

### Scenario 2 — Aisha-style (open now)

**P1:** Did not notice the open-now filter. Searched "food",
scanned the results, and read the "Open now" / "Closed now" labels
on individual cards to determine which to visit. Eventually found
one that was open and read the closing time off the detail page.
Took longer than P2 (~3 minutes).

**P2:** Same approach — did not see the filter, used the per-card
labels instead. Completed faster than P1 (~1 minute).

**Common finding:** the per-card open-now labels are doing the
filter's job from the user's perspective. The filter itself is
invisible.

### Scenario 3 — ESOL (English classes)

**P1:** Searched "english classes", found two results, clicked into
one for enrolment information. Read the eligibility notes, noted
they would need to contact the organisation.

**P2:** Identical approach, slightly faster.

**Common finding:** the lack of specific class times (the data
is marked needs_verification) did not block either participant,
they understood the "contact to enrol" instruction.
