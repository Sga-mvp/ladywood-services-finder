# Requirements

This document brings together the functional and non-functional requirements
of the Ladywood Community Services Finder. The functional requirements are
derived from the user stories in [`user-stories.md`](user-stories.md);
non-functional requirements come from the personas in
[`personas.md`](personas.md), the MoSCoW analysis in [`moscow.md`](moscow.md),
and the sustainability analysis in [`sustainability.md`](sustainability.md).

The intent is to make it possible for a non-author reader to understand precisely what the v1 system was meant
to do and what was deliberately scoped out.

---

## Functional requirements

Functional requirements describe what the system does. Each one traces to
the user story or stories that gave rise to it. The acceptance criteria for
each story live in [`user-stories.md`](user-stories.md) in Given/When/Then
form, and each Must-have user story has at least one corresponding
automated test in `tests/`.

### Resident-facing (the search side)

| ID | Requirement | Story |
|----|-------------|-------|
| FR-1 | The system shall present a homepage with a free-text search box and a list of category quick-tap tiles. | US-01, US-02, US-05 |
| FR-2 | The search shall accept a `need` query string parameter and return services whose categories match by slug or display-name substring. | US-05 |
| FR-3 | The search shall accept an `open_now` flag and, when set, exclude services that are not open at the current local time. | US-04 |
| FR-4 | Each search result shall display the service name, a plain-English description, address, postcode (if known), and eligibility labels. | US-03, US-06 |
| FR-5 | Eligibility shall be shown as visible labels on each result card. Specifically: drop-in, voucher needed, referral needed, currently open / closed. | US-06 |
| FR-6 | Each service shall have a detail page showing full opening hours for the week, eligibility notes, contact information (phone, website), and provenance (data source, last updated). | US-03, US-20 |
| FR-7 | Services marked inactive shall not appear in search results but shall remain reachable by direct URL, with a clear "currently closed" banner. | US-16 (admin), US-20 (resident) |
| FR-8 | The system shall require no user account, no email collection, and no login of any kind for any resident-facing flow. | US-01 |

### Org-admin-facing (the management side)

| ID | Requirement | Story |
|----|-------------|-------|
| FR-9 | The system shall provide a login page accepting email and password. Authentication shall be session-based. | US-15 |
| FR-10 | Authenticated admins shall see a list of all services with options to add a new service or edit an existing one. | US-13, US-14 |
| FR-11 | The add-service form shall require name, description, and address; postcode, eligibility booleans, and notes are optional. | US-13 |
| FR-12 | The edit-service form shall provide an `is_active` toggle that, when unticked, marks the service as temporarily closed and excludes it from resident searches. | US-16 |
| FR-13 | Every save shall display a visible confirmation message ("saved" / "added" / etc.). | US-17 |
| FR-14 | Admin-only routes shall redirect unauthenticated requests to the login page. | US-15 |
| FR-15 | Logout shall clear the session entirely and be triggered via a POST request only. | US-15 |

---

## Non-functional requirements

Non-functional requirements describe how the system behaves; performance,
accessibility, security, maintainability. These are mostly derived from the
personas rather than from individual stories.

### Accessibility (WCAG-aligned)

| ID | Requirement | Source |
|----|-------------|--------|
| NFR-1 | Body text shall be at least 18px (1.125rem) at the default zoom level. | Margaret persona, US-02 |
| NFR-2 | Contrast ratio between body text and background shall meet WCAG AAA (≥7:1). | Margaret persona, US-02 |
| NFR-3 | All interactive elements shall have a focus indicator of at least 3px. | NFR-1, NFR-2 baseline |
| NFR-4 | Touch targets shall be at least 44×44px (WCAG 2.5.5). | Mobile use |
| NFR-5 | Pages shall remain functional and readable at 200% browser zoom with no horizontal scrolling. | Margaret persona, US-02 |

### Performance and connectivity

| ID | Requirement | Source |
|----|-------------|--------|
| NFR-6 | The resident-facing pages shall be interactive within 3 seconds on a simulated 3G connection (1.6 Mbps down, 300ms RTT). | Aisha persona, US-07 |
| NFR-7 | The resident search flow shall function with JavaScript disabled. | Aisha persona, Mahmoud persona, US-07 |
| NFR-8 | Pages shall be printable to one A4 sheet with site chrome removed. | Mahmoud persona, US-12 |

### Privacy and ethics

| ID | Requirement | Source |
|----|-------------|--------|
| NFR-9 | The system shall not include third-party tracking, analytics, fonts, or advertising. | US-19 |
| NFR-10 | The system shall not store any resident-side identifying data (no accounts, no IP logging beyond default webserver behaviour). | US-01, US-19 |
| NFR-11 | Admin passwords shall be hashed with a salted algorithm; plaintext passwords shall never be stored. | Standard security |

### Maintainability

| ID | Requirement | Source |
|----|-------------|--------|
| NFR-12 | Every entity in the data model shall correspond to one class in the UML class diagram. | Class diagram is source of truth |
| NFR-13 | Every functional Must-have requirement shall have at least one automated test that verifies its acceptance criteria. | Testing rubric (10%) |
| NFR-14 | The application shall run on the dependency versions pinned in `requirements.txt`; no unpinned dependencies. | Reproducibility |
| NFR-15 | Every commit to `main` shall be tested by CI on at least two Python versions. | Reproducibility |

### Data quality

| ID | Requirement | Source |
|----|-------------|--------|
| NFR-16 | Each service entry shall record its data source (URL or document reference). | Honesty about provenance |
| NFR-17 | Services with unverified or incomplete information shall be flagged with `needs_verification: true`. | Honesty about limits |
| NFR-18 | Services that have closed shall be retained with `is_active: false` rather than deleted. | NFR-16 supports this |

---

## Constraints and assumptions

### Constraints (things we cannot change)

- **Timeline:** Eight working days from 3 June 2026 to the 11 June deadline.
- **Team:** Solo, with lecturer-approved fallback recorded in
  [`lecturer-correspondence.md`](lecturer-correspondence.md) (when added).
- **Brief restriction:** The EWB brief explicitly forbids contacting actual
  Ladywood residents. All user testing is conducted with external participants
  (not residents of Ladywood) running scripted persona scenarios.
- **Tech stack:** Python 3.11+, Flask, SQLAlchemy, SQLite, pytest, GitHub
  Actions. Pinned in `requirements.txt` and `.github/workflows/ci.yml`.

### Assumptions (things we are taking as given)

- The information about each seeded service was accurate at the date of
  compilation (2026-06-07). Opening hours and eligibility may change.
- The list of services is representative of the Ladywood Ward and immediate
  surrounds but is not exhaustive. A production system would source data
  from a council or NNS feed, not a one-off compilation.
- The org-admin role (Sarah) operates a single organisation in v1. Multi-org
  admin (different admins for different services) is a v2 concern.
- The system's UI language is English. Non-English speakers are supported
  through the "languages spoken" field on services (when populated) and
  through browser-level translation tools (which work well with
  server-rendered HTML).

### What this is *not*

- Not a benefits eligibility calculator.
- Not a chatbot.
- Not a social network or peer-support platform.
- Not a replacement for human caseworkers or advice services.
- Not a production-ready deployment. The prototype demonstrates the
  approach, not the operational readiness.

---

## Acceptance criteria summary

The system is considered to satisfy v1 when:

1. All seven Must-have user stories (US-01, US-03, US-04, US-05, US-06,
   US-13, US-17) pass their automated acceptance tests.
2. The seeded database loads cleanly via `python -m src.seed_loader`.
3. CI is green on every commit to `main`.
4. External user testing has been conducted with at least three participants
   and the results are recorded in `docs/user-testing.md`.
5. The presentation slides reference each user story in the demo walkthrough.

At time of writing, items 1–3 are complete; items 4–5 are in progress.
