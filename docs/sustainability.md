# Sustainability Analysis

*To be drafted.*

The brief weights sustainability at 10% and asks for it to be considered in
**both design and implementation**, and optionally in the development process
itself. This document will cover:

- **Energy and compute** — server-light architecture, no client-side JS for
  core flows, SQLite rather than a database server, no third-party tracking.
- **Hardware** — the prototype targets old Android devices and library-grade
  computers, not the newest hardware.
- **Materials** — not applicable as a software-only prototype, but discussed
  in relation to device lifespan and the Birmingham Device Bank.
- **Longevity and maintainability** — code structured for handover, documented,
  with tests so future maintainers can change it safely.
- **Accessibility as sustainability** — a system unusable by 28.6% of residents
  is socially unsustainable regardless of its energy profile.
- **Development process** — version control, CI, AI usage logged, decisions
  recorded in commits and design docs.
