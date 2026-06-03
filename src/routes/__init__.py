"""
Route handlers, grouped by feature.

Each feature lives in its own module and exposes a Flask Blueprint that is
registered in src/app.py. Suggested blueprints:

  - search.py   — resident-facing search and result pages
  - admin.py    — org-admin login, service create/edit/delete
  - api.py      — JSON endpoints (if any are needed beyond server-rendered HTML)
"""
