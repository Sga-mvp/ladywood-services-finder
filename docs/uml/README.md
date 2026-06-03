# UML Diagrams

*To be drafted.*

Four diagrams are planned, chosen because they each earn their place in the
design and feed something downstream. Padding the count with diagrams that
don't carry weight (e.g. deployment diagrams for a single-process prototype)
is avoided.

1. **`use-case.png`** — Use case diagram. Actors (Resident, Org Admin, System)
   and the main use cases. Anchors the requirements doc.

2. **`class-model.png`** — Class / domain model. Service, Location,
   OpeningHours, EligibilityRule, Language, OrgAdmin. Drives the SQLAlchemy
   model in `src/models.py`.

3. **`search-sequence.png`** — Sequence diagram for the core
   "resident searches by need" flow. Clarifies where the matching logic lives
   and what calls what.

4. **`opening-hours-activity.png`** — Activity diagram for the
   "is this service open right now?" decision, including bank holidays,
   by-appointment-only services, and voucher windows. Drives the test cases
   for the opening-hours module.

Diagrams will be drafted in draw.io (or similar) and exported as PNG. Source
`.drawio` files will be committed alongside the PNGs so they remain editable.
