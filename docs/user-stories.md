# User Stories

User stories derived from the personas in [`personas.md`](personas.md). Each story is given an ID (US-NN) so it can be referenced from the MoSCoW analysis, the UML diagrams, and the test suite.

Acceptance criteria are written in **Given / When / Then** form. They define what "done" means for each story and are the source of truth for both implementation and testing — every Must-have story (see [`moscow.md`](moscow.md)) should have a corresponding automated or manual test that traces back to its acceptance criteria.

The stories are weighted toward residents (the people the project exists to serve) rather than the org-admin stakeholder. Resident stories: 13. Org-admin stories: 5. Cross-cutting (non-functional, persona-agnostic): 4.

---

## Margaret — older resident, post-library closure

### US-01 — Find a service without creating an account

**As Margaret, I want to find help without signing up or giving my email, so that I can use the site immediately without fearing I've committed to something.**

- *Given* I land on the homepage for the first time,
- *When* I look at the page,
- *Then* I see the search interface immediately, with no banner, popup, login prompt, or cookie wall asking me for personal information.

- *Given* I have completed a search and clicked a result,
- *When* I view the service details,
- *Then* I am not asked to register, log in, or provide an email at any point.

### US-02 — Read everything at a comfortable text size

**As Margaret, I want the text on the page to be large enough to read without my glasses, so that I don't give up before I've started.**

- *Given* I open the site on any device,
- *When* the page loads,
- *Then* the default body text is at least 18px (1.125rem) and the contrast ratio between text and background is at least 7:1 (WCAG AAA).

- *Given* I zoom my browser to 200%,
- *When* the page redraws,
- *Then* the layout still works — no horizontal scrolling, no overlapping text, no hidden buttons.

### US-03 — Understand what each service is before I click

**As Margaret, I want each result to explain what the service is in plain English, so that I don't waste a trip to somewhere that turns out to be the wrong place.**

- *Given* a search returns one or more results,
- *When* I look at a result card,
- *Then* I see the service name, a one-sentence plain-English description (reading age ≤ 9), the address, and the next opening time.

---

## Aisha — single parent, time-pressed

### US-04 — Find services that are open right now

**As Aisha, I want to filter for services that are open at this moment, so that I don't waste data and time on places that turn out to be closed.**

- *Given* the current time is 14:30 on a Tuesday,
- *When* I search and tick "Open now",
- *Then* the results show only services whose Tuesday opening hours include 14:30.

- *Given* it is a recognised bank holiday (e.g. Christmas Day),
- *When* I search with "Open now" enabled,
- *Then* the results exclude any service that has not explicitly declared bank-holiday opening hours.

### US-05 — Search by what I need, not by category name

**As Aisha, I want to type or tap "food" rather than know that food banks are listed under "Welfare Support", so that I can find help without learning the system's vocabulary.**

- *Given* I tap "food" on the homepage,
- *When* the search runs,
- *Then* I see services tagged with `food`, `food-bank`, `meals`, `pantry`, or `community-kitchen`, ranked with closest first.

- *Given* I type a colloquial term like "fed up and cold",
- *When* the search runs,
- *Then* the system either returns relevant warm-space results or, if it cannot, displays a clear "no results — try one of these categories" message with tappable category buttons.

### US-06 — Know whether I need a voucher before I travel

**As Aisha, I want to see eligibility requirements (voucher, referral, drop-in) on the result card, so that I don't arrive somewhere and be turned away in front of my kids.**

- *Given* a service requires a voucher or referral,
- *When* it appears in my search results,
- *Then* the card shows a visible "Voucher needed" or "Referral needed" label, with a link to "How to get a voucher" if available.

- *Given* a service is drop-in with no requirements,
- *When* it appears in my search results,
- *Then* the card shows a "Drop-in — no voucher needed" label.

### US-07 — Use the site on a slow connection

**As Aisha, I want pages to load quickly even when my data is low, so that the site is useful in the moments I most need it.**

- *Given* a simulated 3G connection (1.6 Mbps down, 750 Kbps up, 300ms RTT),
- *When* I load the homepage,
- *Then* the page is interactive within 3 seconds.

- *Given* I have JavaScript disabled in my browser,
- *When* I search,
- *Then* the search still works and returns results.

### US-08 — See walking distance, not driving time

**As Aisha, I don't own a car, so I want to see how far a service is on foot from where I am, not as a driving estimate.**

- *Given* I have entered or selected a postcode or area,
- *When* the search runs,
- *Then* each result displays walking distance in minutes (rounded to nearest 5) and the result is filtered to within a configurable radius (default 20 minutes).

---

## Mahmoud — recent migrant, limited English

### US-09 — Find services in my language

**As Mahmoud, I want to filter for services where staff speak Arabic, so that I'm not turned away or misunderstood when I arrive.**

- *Given* I select "Arabic" from a language filter,
- *When* the search runs,
- *Then* the results show only services where Arabic is listed in the `languages_spoken` field, OR services explicitly tagged as "interpreter available on request".

### US-10 — Read service descriptions in my own language

**As Mahmoud, I want at least the core service information in Arabic, so that I can understand what the service is without relying on Google Translate for every word.**

- *Given* I switch the interface language to Arabic via a visible language picker,
- *When* any page reloads,
- *Then* the UI labels (buttons, filter names, headings) appear in Arabic and the layout adjusts for right-to-left reading.

- *Given* a service entry has an Arabic translation provided,
- *When* I view the service in Arabic mode,
- *Then* the description, eligibility, and access notes display in Arabic. Where translation is not available, the English text displays with a clearly-labelled "Translation not available" notice.

### US-11 — Know whether a service is culturally appropriate

**As Mahmoud, I want to know whether a food parcel includes halal options, or whether men and women are seen separately, so that I can use services that match my family's needs.**

- *Given* a service has cultural notes set by its admin,
- *When* I view the service details,
- *Then* I see a "Cultural notes" section showing free-text information such as "halal options available" or "separate sessions for women on Wednesdays".

### US-12 — Print a page when I can't keep using the internet

**As Mahmoud, my home wifi is unreliable, so I want to print a service's address and opening times to take with me, so that I don't need internet to find the place later.**

- *Given* I am on a service detail page,
- *When* I press my browser's print function (Ctrl/Cmd+P),
- *Then* the printed page shows the service name, address, opening hours, eligibility, and a small map or directional note — fitting on one A4 page, without navigation chrome or ads.

---

## Sarah — voluntary-sector coordinator

### US-13 — Add my service to the directory

**As Sarah, I want to add my organisation's service to the directory in under 5 minutes, so that listing my service doesn't become another job.**

- *Given* I have an org-admin account,
- *When* I click "Add a service" and fill in the required fields (name, description, address, opening hours, eligibility, languages),
- *Then* the service is saved and immediately visible in resident searches.

### US-14 — Update opening hours quickly

**As Sarah, my volunteer rota changes weekly, so I want to update opening hours without re-entering anything else.**

- *Given* I am logged in and viewing my service's edit page,
- *When* I change only the opening hours field and click "Save",
- *Then* the change is saved without me having to confirm or re-enter any other field, and the change is visible in resident searches within 1 minute.

### US-15 — Log in without remembering a complicated password

**As Sarah, I run a small organisation and don't want a 2FA hurdle every time I update opening hours.**

- *Given* I have registered with email and password,
- *When* I log in with valid credentials,
- *Then* I am logged in without being prompted for a second factor on v1. (2FA is a future enhancement, not a v1 requirement.)

### US-16 — Mark my service as temporarily closed

**As Sarah, sometimes a session is cancelled at short notice, so I want to mark my service as "temporarily closed" without deleting it.**

- *Given* I am editing my service,
- *When* I tick "Temporarily closed" and provide a reason,
- *Then* the service appears in resident searches with a clear "Temporarily closed: [reason]" banner, and is excluded from "Open now" filters.

### US-17 — Trust that my changes are saved

**As Sarah, I want clear confirmation when I save changes, so that I don't go away wondering if it worked.**

- *Given* I save any change,
- *When* the save completes,
- *Then* I see a visible confirmation message ("Saved at 14:32") and the change is reflected in the form fields.

---

## Cross-cutting / non-functional

### US-18 — Use the system on any device

**As any user, I want the site to work on whatever device I have, so that I'm not blocked by needing a specific phone or browser.**

- *Given* I open the site on a 5-year-old Android phone (Android 9+), an iPhone (iOS 14+), a Windows laptop, or a library computer (modern Chrome/Firefox),
- *When* the page loads,
- *Then* the layout is usable and all core flows (search, view result, view detail) work.

### US-19 — Avoid being tracked

**As any user, I don't want my visit to be tracked by third-party analytics, advertisers, or social networks, so that using the site does not put me on databases I didn't consent to.**

- *Given* I load any page,
- *When* I inspect network traffic,
- *Then* no requests are made to third-party domains (Google Analytics, Facebook, Twitter, advertising networks). All assets (CSS, fonts, scripts) are served from the application's own domain.

### US-20 — Know the system is up to date

**As any user, I want to know how recently a service's information was checked, so that I can judge whether to trust it.**

- *Given* I view a service detail page,
- *When* the page loads,
- *Then* I see "Last updated: [date]" prominently displayed.

### US-21 — Find help if the system can't help me

**As any user, when the search returns nothing useful, I want to know where else to go, so that the system doesn't leave me stuck.**

- *Given* a search returns zero results,
- *When* the empty-state appears,
- *Then* it shows a clear message ("We don't have a match — try a different search or contact one of these general helplines") with 2–3 verified national/regional helpline numbers (e.g. Citizens Advice, Samaritans, NHS 111).

---

## Story-to-persona traceability

| Persona | Story IDs |
|---|---|
| Margaret | US-01, US-02, US-03 |
| Aisha | US-04, US-05, US-06, US-07, US-08 |
| Mahmoud | US-09, US-10, US-11, US-12 |
| Sarah | US-13, US-14, US-15, US-16, US-17 |
| Cross-cutting | US-18, US-19, US-20, US-21 |

Every primary persona has at least three stories. No story exists without a persona-driven justification.

## Next steps

- These stories feed into [`moscow.md`](moscow.md), where each is classified as Must / Should / Could / Won't for v1.
- Must-have stories drive the class diagram in `uml/` (every entity needed to satisfy a Must must appear in the model).
- Acceptance criteria translate directly into pytest test cases — every Must-have story should have at least one automated or manual test that verifies its acceptance criteria.
