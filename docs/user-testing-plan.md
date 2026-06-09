# User Testing Plan

This document is the plan I will follow when conducting external user
testing on the Ladywood Community Services Finder prototype. Findings
will be written up in `user-testing-results.md` after the sessions run.

## Why we are testing

The brief explicitly forbids contacting actual Ladywood residents. External
user testing therefore uses people not connected to the project (housemates,
family, fellow students from other courses) who are asked to play through
scenarios based on the personas in `personas.md`.

Two things are being assessed:

1. **Task completion** — can a non-author user complete a task that one of
   the personas would realistically attempt, without help?
2. **Comprehension and trust** — do users understand what they are seeing
   on each screen? Do they trust the data? Would they actually use it?

The acceptance criteria in `user-stories.md` are the source of truth for
what each persona is trying to do.

## Who I am recruiting

Three participants, chosen as a mix of persona-match and convenience:

| # | Persona-aligned with | Why this person | Rough age | Tech comfort |
|---|---------------------|------------------|-----------|--------------|
| P1 | Margaret (older resident, post-library) | A grandparent / older relative who uses a smartphone but is not a confident web user | 60+ | Low–medium |
| P2 | Aisha (time-pressed parent) | A friend / family member who is busy and has children, used to mobile apps | 30–45 | High |
| P3 | Convenience | A fellow student or housemate who is not on this module | 18–25 | High |

P1 is the most important to recruit well: Margaret's persona is the one
most at risk of being designed-around in an undergraduate computing project.
If only P2 and P3 can be found, the plan flags this as a limitation in the
writeup.

## What I am NOT doing

- Not contacting any Ladywood resident (per the brief).
- Not running this on more than three people — additional participants
  add little new signal at this scale and consume disproportionate time.
- Not running A/B tests or quantitative experiments. The sample is too
  small for that to be meaningful.
- Not testing the org-admin (Sarah) flow with external participants.
  Volunteers running a community organisation are out of reach in the
  timeline; the admin flow has automated tests instead.

## Test environment

- The prototype running on my laptop (`flask --app src.app run --port 5001`)
  with the seeded 13 services loaded.
- Each participant uses their own device, phone or laptop, connected to
  the laptop's network. This mirrors how a real resident would access the
  service.
- I will be present, observing, but not helping unless the participant is
  fully stuck for more than 90 seconds.

## What I will record

For each session, per scenario:

- **Did the participant complete the task?** (Yes / Partially / No)
- **Time taken** (rough estimate, not stopwatch — to the nearest 30s)
- **Where they hesitated or backtracked** (free-text note)
- **What they said out loud** (asked them to think aloud as they go)
- **What they thought the system was doing** at points of confusion
- **One-line follow-up question** after each task — see scenarios below

No identifying information is recorded. Participants are referred to as
P1, P2, P3 throughout.

## Consent

Before each session, the participant is told:

- This is a final-year university project, not a real public service.
- I will be watching what they do and writing notes.
- No information about them personally will be recorded, just observations
  about what worked and didn't work in the prototype.
- They can stop at any time.
- The notes will appear in my university coursework.

Verbal consent is obtained and noted in the writeup.

---

## Scenarios

Three scenarios, each takes 3–5 minutes. The full session per participant
is roughly 20 minutes including consent and follow-up.

### Scenario 1 — Margaret-style (from US-01, US-03)

**Setup brief read aloud to participant:**

> "Imagine you have just heard from a neighbour that there are food banks
> in your area in Ladywood, Birmingham. You do not have an account or
> email signed up for anything. Find a food bank you could go to and tell
> me one piece of practical information about it, for example, its
> address, or whether you need a voucher to use it."

**What I am watching for:**

- Did they reach a search result without being asked to sign up? (US-01)
- Did they tap a category or type into the search box?
- Could they tell at a glance whether a food bank needed a voucher? (US-06)
- Did the descriptions read clearly to them, or did they ask "what does
  this mean?" (US-03)
- Did they end the task feeling they had a useful answer?

**Follow-up question:**

> "If you were doing this for real, would you trust what you just saw, or
> would you want to phone someone to check?"

### Scenario 2 — Aisha-style (from US-04, US-05, US-06)

**Setup brief:**

> "It is now [the actual time of the test]. You urgently need to find
> somewhere offering food that is open at this moment, that does not
> need you to get a voucher first. Find one and tell me where it is and
> when it closes today."

**What I am watching for:**

- Did they spot or use the 'open now' filter? (US-04)
- Did they understand the difference between voucher-required services
  and drop-in services from the result cards? (US-06)
- Did they search by "food" rather than the underlying category names? (US-05)
- If results were sparse, did they untick "open now" themselves, or did
  they assume the system had nothing to offer?

**Follow-up question:**

> "If you couldn't find a place that was open right now, what would you
> have done next?"

### Scenario 3 — Convenience / ESOL learner (from US-05)

**Setup brief:**

> "Imagine you have a relative who has recently moved to Birmingham and
> speaks limited English. They are looking for somewhere they can take
> English language classes for free. Find at least one option and tell
> me how they would enrol."

**What I am watching for:**

- Did the search term "english" or "language" return the ESOL services? (US-05)
- Did they read the eligibility notes for enrolment information? (US-03)
- Did they spot the `needs_verification` honesty markers or the "contact
  to enrol" notes?
- Did they ever go into the service detail page or stop at the result card?

**Follow-up question:**

> "From what you saw, did you trust that the information was up to date?
> What made you think yes or no?"

---

## What success looks like

Per scenario, the task is **completed** if the participant ends with an
answer that matches an actual service in the seed data without my help.

Per session, the overall finding I am looking for is the answer to:

> "Could this person, with the information they had on screen, actually
> go and use one of these services in real life?"

The writeup in `user-testing-results.md` will summarise:

- Completion rates per scenario (3/3, 2/3, etc.)
- Three things that worked
- Three things that did not
- One thing each participant said that I had not anticipated
- Two concrete changes the testing would prompt me to make in v1.1
- One change so significant it would have changed the v1 scope if known
  earlier

## Limitations the writeup will acknowledge

- Sample size of three is below conventional usability research thresholds
  (typically n=5). Findings are indicative, not statistical.
- No participant matches Mahmoud's profile exactly (recent migrant with
  limited English). The brief's no-contact rule prevents recruiting one.
- I observed the sessions, which probably caused participants to perform
  better than they would unsupervised.
- The seed data has known gaps (`needs_verification: true` on 7 of 13
  services). This may have affected what participants found.

## When this will happen

Sessions are scheduled for [date — fill in when arranged]. The plan and
participants are confirmed by [date]. Writeup committed to the repo
within 24 hours of the final session.
