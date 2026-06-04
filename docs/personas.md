# Personas

Four personas drive the design: three resident archetypes (primary users) and one voluntary-sector org admin (secondary stakeholder). All names are invented; demographics are drawn from the 2021 Census data and the EWB brief's statistics for the Ladywood Ward and Parliamentary Constituency.

These personas are deliberately concise. Each ends with a *design implication* — the line a developer needs to read to know what to build differently because of this person.

---

## Margaret, 71 — older resident, post-library closure

- Widowed, lives alone in a Ladywood council flat. One of the 49.8% of one-person households in the ward.
- Used Springhill Library twice a week for years — for the warm space, the staff who helped her fill in forms, and free internet to video-call her daughter in Manchester. It closed in 2024.
- Has a basic smartphone her daughter set up. Uses it for calls and WhatsApp; everything else feels "designed to trip her up". Has never installed an app herself.
- Her pension covers rent and food but not heating both rooms in winter. Worries about being one of the 26.6% of households in fuel poverty.
- Trusts: her GP, the postman, the woman at the corner shop. Distrusts: anything that asks for an email address before it tells her what it is.
- **Design implication:** *No account, no app install, no email field on the resident flow. Large text, high contrast, plain English at reading age 9. The system has to be useful in the first 10 seconds or she closes it.*

---

## Aisha, 34 — single parent, time-pressed, in crisis

- Lives with three children in a privately rented flat in Ladywood. Two of her children are affected by the two-child benefit cap (Ladywood has the second-highest proportion in the UK).
- Her hours at a care home were cut last month. Has used a food bank twice; finds it shaming and only goes when there's no other option. Needed a voucher from a support worker the first time and didn't know where to get one the second.
- Smartphone-confident — uses WhatsApp, TikTok, the bus app, her bank. But her data runs out before the end of the month and she rations it.
- Has roughly 3 minutes between school pickup and the next thing to figure out where she's getting dinner from tonight. Doesn't have time to read a paragraph.
- English is her first language. Reads quickly when content is direct; switches off when content feels patronising or bureaucratic.
- **Design implication:** *Speed is the feature. "Open now, walking distance, voucher needed yes/no" must be visible without scrolling. The system has to work on a slow connection and degrade gracefully when she has 30MB of data left for the month. No shame in the copy — services, not "help for people like you".*

---

## Mahmoud, 58 — recent migrant, limited English

- Arrived in Birmingham 18 months ago from Sudan via the asylum process; now has leave to remain. Living in temporary accommodation in Ladywood. One of the ~28,000 migrants who have registered with a GP in the constituency in recent years.
- Spoke fluent Arabic and functional French before arrival. English is his fourth language and he is one of the 3.8% of Ladywood residents who say they cannot speak English well.
- Has an old Android phone, prepaid SIM, intermittent wifi in the accommodation. Google Translate is open in another tab whenever he uses the internet.
- Trained as a teacher in Sudan; cannot work in the UK yet. Wants to find: an English class, a halal food bank or food parcels he can use, somewhere to print documents for his immigration solicitor.
- Cultural context matters — needs to know whether a service is faith-aware, whether women and men are seen separately, whether his children would be welcome.
- **Design implication:** *Multilingual matters but is more than translation — service entries need fields for "languages spoken by staff/volunteers" and free-text cultural notes. Icons and pictographs alongside text help when reading is slow. The system must work without JavaScript because his accommodation wifi is unreliable and full pages reload faster than partial ones over flaky connections.*

---

## Sarah, 42 — voluntary-sector coordinator (secondary stakeholder)

- Runs a small Neighbourhood Network Scheme partner organisation from a shared office near Five Ways. Has a part-time admin who comes in two mornings a week.
- Manages: their food parcel service, weekly digital-help drop-in, occasional English conversation circles. Hours and eligibility change month to month based on volunteer availability.
- Confident with computers — uses Microsoft 365, runs a Mailchimp newsletter, edits a basic Wix site once a quarter. Not a developer. Has no budget for one.
- Frustration: people turn up on days the service isn't running because the information they found online is out of date. She has no time to update five different directories.
- Knows the residents her service serves. Will resist anything that frames her clients as helpless or her organisation as low-status.
- **Design implication:** *The org-admin interface needs to be simpler than her Wix editor, accessible from any browser, and editable in under 2 minutes for a routine change like opening hours. No technical jargon, no "deploy" or "publish" — just "save". Authentication must exist but must not be onerous (email + password is fine; no 2FA on v1).*

---

## How these personas are used downstream

- **Requirements / user stories** are written from these personas' perspectives, in the form *"As [persona], I want to [action] so that [outcome]."*
- **MoSCoW** decisions explicitly reference the personas — a feature is a Must only if at least one of the three resident personas would fail their primary task without it.
- **Acceptance criteria** for Must-have features describe behaviour that a developer can verify a persona's needs are met.
- **User testing** (with external participants, not Ladywood residents — per the brief's no-contact rule) uses scenarios drawn from these personas to ensure the prototype actually serves the people it claims to.
