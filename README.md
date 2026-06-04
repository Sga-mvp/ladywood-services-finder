# Ladywood Community Services Finder
![CI](https://github.com/Sga-mvp/ladywood-services-finder/actions/workflows/ci.yml/badge.svg)
A lightweight, low-bandwidth service-discovery prototype for vulnerable residents in Ladywood, Birmingham. Built as part of the UEA Launchpad Year 2 project, addressing the EWB Engineering for People Design Challenge 2025–26.

## What it does

Helps a resident find an open, walkable, eligible community service (food bank, warm space, digital support, language help, benefits advice) for a stated need, without requiring an account, an app, or fast internet.

See [`docs/problem-statement.md`](docs/problem-statement.md) for the full context, target users, and scope.

## Status

Prototype, in active development. Not production software. Not affiliated with CIVIC SQUARE, Engineers Without Borders, or any Ladywood community organisation — this is an educational project.

## Tech stack

- **Python 3.11+**
- **Flask** — web framework
- **SQLAlchemy** — ORM
- **SQLite** — database (file-based, no server required)
- **Jinja2** — server-side templates (works without JavaScript)
- **pytest** — test framework
- **GitHub Actions** — continuous integration

The stack is deliberately minimal. The whole system is designed to run on modest hardware with no external services, in line with the sustainability brief.

## Local setup

Requires Python 3.11 or newer.

```bash
# clone the repo
git clone <repo-url>
cd ladywood-services-finder

# create a virtual environment
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# run the app
flask --app src.app run --debug
```

The app will be available at http://localhost:5000.

## Running tests

```bash
pytest
```

Tests run automatically on every push via GitHub Actions — see [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Project structure

```
.
├── src/                 # application code
│   ├── app.py           # Flask app factory
│   ├── models.py        # SQLAlchemy data model
│   ├── routes/          # route handlers, grouped by feature
│   ├── templates/       # Jinja2 HTML templates
│   └── static/          # CSS, any static assets
├── tests/               # pytest test suite
├── docs/                # design documents
│   ├── problem-statement.md
│   ├── personas.md
│   ├── requirements.md
│   ├── uml/             # UML diagrams
│   ├── ai-usage-log.md
│   └── sustainability.md
├── .github/workflows/   # GitHub Actions CI
├── requirements.txt
└── README.md
```

## Design documents

- [Problem statement](docs/problem-statement.md)
- Personas — *to be added*
- Requirements & MoSCoW — *to be added*
- UML diagrams — *to be added*
- Sustainability analysis — *to be added*
- [AI usage log](docs/ai-usage-log.md)

## Licence

Educational use. No licence granted for commercial reuse.
