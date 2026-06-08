# Sustainability Analysis

The EWB Engineering for People brief frames sustainability through the
Doughnut Economics lens: meeting human needs (social foundation) without
overshooting planetary boundaries (ecological ceiling). This analysis
considers the project on three axes:

1. **Ecological** — energy, materials, hardware, network demand
2. **Social** — accessibility, inclusion, longevity for the people served
3. **Process** — sustainability of the development process itself

Each axis covers what was considered, what was built, and what was
deliberately scoped out.

---

## 1. Ecological sustainability

### Server-light architecture

The application is a single Flask process backed by a SQLite database file.
There is no database server, no caching layer, no message queue, no
container orchestration. The whole system runs on hardware that
is already in use somewhere, an old laptop, a Raspberry Pi, a shared
hosting account. This was a deliberate choice over heavier alternatives
(Django + Postgres + Redis) which would have consumed more energy per
request and required dedicated infrastructure.

### Page weight and network demand

The resident-facing pages are server-rendered HTML with one CSS file and
no JavaScript. There are no images on the search and result pages. The
homepage renders in under 10kB of HTML and roughly 8kB of CSS, both
gzip-compressible.

This matters ecologically because every byte transmitted consumes energy at
every hop of the network. It matters socially because Aisha (US-07) is
rationing her mobile data, a lighter page is a more sustainable page in
both senses.

### No third-party tracking, no analytics, no advertising

US-19 records this as a Should-level requirement; in v1 it is implemented
by simply not adding anything. There are no Google Analytics tags, no
Facebook pixels, no advertising network calls, no CDN-hosted fonts (system
fonts are used). The user's request goes to one server and comes back. No
energy is spent that the user did not consent to.

### Hardware target

The site is designed to work on five-year-old Android phones (US-18), on
library-grade computers (US-18), and on assistive technologies (screen
readers, browser zoom). This extends the useful life of existing hardware
and reduces pressure on the resident to upgrade.

### Trade-offs and limits

The system stores all data in one SQLite file. This is appropriate for a
prototype but does not scale to many concurrent writers. A v2 deployment
serving multiple voluntary-sector partners would need Postgres or similar,
with the energy cost that implies. The decision is to accept that as a
later cost rather than over-engineer now.

### What was *not* done

- No image optimisation (because there are no images yet).
- No service-worker offline cache (US-07's offline functionality is
  scoped out of v1; would be a v2 feature).
- No SSR-skipping caching layer (page generation cost is low enough that
  caching adds energy use rather than removing it at this scale).

---

## 2. Social sustainability

### Accessibility as a sustainability concern

A system unusable by 28.6% of Ladywood's residents (the proportion whose
first language is not English) is socially unsustainable regardless of its
energy profile. The design treats accessibility as a primary axis, not a
post-hoc addition:

- **Reading age and language:** Plain English used throughout. Service
  descriptions are limited to 280 characters to keep them scannable.
- **Visual accessibility:** Base font size 18px, line-height 1.6, contrast
  ratio of body text on background is 17:1 (WCAG AAA, well above the
  required AA threshold of 4.5:1). All focus rings 3px and clearly visible.
- **Touch-target accessibility:** All clickable elements meet the WCAG 2.5.5
  minimum of 44×44px on mobile.
- **No-account access:** Margaret (US-01) faces no login wall, no email
  collection, no cookie banner. The system is usable in the first ten
  seconds.
- **No-JavaScript operation:** The resident search flow is fully functional
  with JavaScript disabled, which protects users on the oldest devices and
  in restricted browser environments.
- **Print fallback:** A `@media print` stylesheet ensures Mahmoud (US-12)
  can print a service's address and opening hours without site chrome,
  for use when home wifi is unreliable.

### Service longevity

The data model deliberately preserves history. Closed services (Spring
Hill Library, Ladywood Share Shack) remain in the directory marked
`is_active: false` rather than being deleted. This serves two purposes:

1. Residents who arrive via an old link or bookmark see "this service is
   no longer running" rather than a 404, which is both more useful and
   more dignified.
2. The dataset becomes a quiet record of community-infrastructure loss.
   Two of the thirteen seeded services are already closed; this matters
   for the people of Ladywood and is itself sustainability evidence.

### Privacy and dignity

The system stores no resident-side data at all; no accounts, no search
history, no IP logging beyond what the underlying webserver does by
default. A vulnerable person using the system at a library computer does
not leave a trail. Sarah's admin account stores only email and a hashed
password (no plaintext, no name, no phone). This is conservative by
design; collecting nothing means there is nothing to lose, leak, or
weaponise.

### Cultural appropriateness

The personas drove the inclusion of structured fields like
`requires_voucher`, `requires_referral`, and free-text `eligibility_notes`
covering things like halal availability and faith-aware practice (US-11).
A directory that listed a halal food bank but did not say so would be
worse than no directory at all.

---

## 3. Process sustainability

### Repeatability and maintainability

The whole project lives in a single Git repository with `requirements.txt`
pinning every dependency to a specific version. Anyone with Python and
git can clone the repo and run the application in under five minutes:

```bash
git clone https://github.com/Sga-mvp/ladywood-services-finder
pip install -r requirements.txt
python -m src.seed_loader
flask --app src.app run --debug
```

The class diagram (`docs/uml/class.png`) is the source of truth for the
data model in `src/models.py`. The activity diagram (`docs/uml/activity.png`)
is the source of truth for the `is_open_at` logic. The user stories
(`docs/user-stories.md`) are the source of truth for the test cases. A
future maintainer who has never seen this codebase can read the design
documents, find the test that covers a behaviour, and change the code
with confidence.

### Continuous integration

Every commit runs the full test suite on two Python versions (3.11 and
3.12) via GitHub Actions. This means a future contributor cannot break
existing behaviour silently, the breaking change is visible on the
commit page before it lands. 46 tests, well under a second to run.

### AI usage transparency

This project used Claude (Anthropic). Every meaningful use
is documented in `docs/ai-usage-log.md`, including what was kept verbatim,
what was edited, and what was explicitly not delegated. Transparency about
AI use is itself a sustainability concern, it preserves the educational
value of the project, allows the marker to assess what was learned.

### Data provenance

Every service in the seed data has a `data_sourced_from` field with a
source URL. Seven of thirteen are marked `needs_verification: true` where
information was incomplete. Two are marked `is_active: false` because
they have closed. This is honest about the limits of the data and gives
a future maintainer a clear starting point for verifying or refreshing it.

---

## What sustainability means here, in one sentence

The most sustainable feature of this system is that it does less, with
less, for a longer period, for people who need it most, and is honest
about all four of those things.

---

## References to module weighting

The brief weights sustainability at 10% of the module mark. It also
states: "consider sustainability in the design and implementation of
your solution, and (optionally) in the engineering of the solution itself."
All three are addressed above. None of this writeup is post-hoc rationalisation,
 each point is implemented in the code or documented in the design.
