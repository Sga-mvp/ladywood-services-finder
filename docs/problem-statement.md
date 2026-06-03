# Problem Statement

**Project:** Ladywood Community Services Finder
**Brief:** EWB Engineering for People Design Challenge 2025–26 — Digital
**Last updated:** 3 June 2026

## The problem in one sentence

In Ladywood, the support that vulnerable residents need most — food banks, warm spaces, digital help, language support, benefits advice — exists, but discovering it on any given day requires the digital literacy, English fluency, and time that the people who need it most are least likely to have.

## Why this matters now

Ladywood is the second most deprived constituency in Birmingham. Specific pressures have made service discovery sharply worse in the last two years:

- **Libraries are closing.** Birmingham City Council declared effective bankruptcy in 2023 and has announced the closure of 25 of 36 libraries citywide. Springhill Library, a short walk from Ladywood, is already closed. Libraries were the primary free route to internet access, printers, and in-person help filling in forms for residents without digital access at home.
- **Digital exclusion is concentrated where deprivation is highest.** Roughly a quarter of West Midlands residents either do not use, or do not have access to, the internet. People earning under £17,499 in Birmingham are 40% less likely to have foundation digital skills than those earning over £50,000.
- **Language is a barrier.** 28.6% of Ladywood residents report a main language other than English; 4.3% cannot speak English well or at all. Most existing service directories are English-only.
- **Demand is up and rising.** 34% of children in the Ladywood Parliamentary Constituency are affected by the two-child benefit cap — the second-highest proportion in the UK. 26.6% of households live in fuel poverty. The 2025 bin strikes and ongoing cost-of-living pressures have pushed more residents toward food banks, warm spaces, and crisis support than the voluntary sector has historically served.

The services to meet this demand do exist — Neighbourhood Network Schemes, voluntary-sector food banks, repair cafés, digital support sessions, the Birmingham Device Bank, the National Digital Inclusion Network — but they are fragmented across dozens of small organisations, listed (where listed at all) on websites that assume a level of digital comfort their target users do not have.

## Who we are designing for

The statement intentionally covers a broad user group at this stage; personas will narrow it. Three resident archetypes drive the design:

1. **Older residents post-library-closure** who previously relied on library staff to help them access services and fill in forms, and who now have neither a trusted in-person route nor the digital confidence to navigate one online.
2. **Families in poverty needing time-sensitive help** — a parent who needs to know which food bank is open this afternoon, whether they need a voucher, and whether the bus fare is worth it.
3. **Recent migrants and residents whose first language is not English**, for whom existing English-only directories are functionally inaccessible even when the underlying service would welcome them.

A fourth, secondary stakeholder is the **voluntary-sector organisation** running a service and wanting to be findable without building and maintaining a website.

We are explicitly **not** designing for: Ladywood residents we contact directly (the brief forbids this), council staff, professional caseworkers, or a national audience. The system is scoped to the Ladywood ward and its immediate surrounds.

## What success looks like

A working prototype where:

- A resident with limited English and an old Android phone can identify an open, walkable, eligible service for their stated need in under a minute, with no account required and no app to install.
- A volunteer at a small community organisation can list, update, and remove a service entry without technical help.
- The system functions on a slow connection, without JavaScript, and degrades to a printable one-page sheet where digital access is not viable.
- The data and matching logic are testable, maintainable, and handed-off in a state where a non-original developer could extend them.

## What this is not

To keep scope honest in an eight-day build window:

- Not a replacement for human support workers, caseworkers, or advice services.
- Not a social network, chat platform, or peer-support forum.
- Not a chatbot or AI assistant; the matching is deterministic and explainable.
- Not a benefits calculator or eligibility decision engine — it surfaces services and their stated eligibility rules but does not advise.
- Not a production system; it is a prototype demonstrating that the approach is viable, contextually appropriate, and sustainable.

## Alignment with the brief

The project addresses the **Digital** challenge area directly, with secondary relevance to **Food** (food-bank discovery), **Built Environment** (warm spaces and community infrastructure), and **Waste** (repair-café and Library-of-Things discovery). It is informed by the case studies of Byng (declining library infrastructure), Khadijah Carberry (storytelling and access), and Eva Bennett (community voice in design).

It aligns with UN Sustainable Development Goals 1 (No Poverty), 10 (Reduced Inequalities), and 11 (Sustainable Cities and Communities), and sits within the *social foundation* lens of the Neighbourhood Doughnut — increasing access to networks, food, and education in a place where those foundations are demonstrably eroded.

## Open questions for the design phase

To be resolved during requirements gathering and persona work, not in this document:

- How is "walking distance" computed without a heavy mapping dependency?
- How are opening-hours edge cases (bank holidays, by-appointment, drop-in only, voucher windows) modelled cleanly?
- What languages are in scope for v1, and how is translation sourced ethically given the no-contact constraint?
- What is the lightest viable authentication model for the org-admin role?
- Where does the seed data come from, and how is its currency maintained beyond the prototype?
