"""
Resident-facing routes.

Implements the Must-have user stories for the resident persona:

    US-01  Find a service without creating an account
    US-03  Understand what each service is before clicking
    US-04  Find services that are open right now
    US-05  Search by need, not category
    US-06  Show eligibility (voucher/referral/drop-in) on result cards

All routes here are GET-only and require no authentication, matching the
"no account required" design principle (US-01). The flow is:

    /           homepage with search form
    /search     results page (also accepts the search submission)
    /service/<id>   full detail page for one service
"""

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, abort, render_template, request

from src.models import Category, Service


bp = Blueprint("search", __name__)


@bp.route("/")
def home():
    """Homepage with the primary search form.

    Shows all available categories so a resident can tap one rather than
    typing — important for Margaret (US-02) and Mahmoud (US-09).
    """
    categories = Category.query.order_by(Category.display_name).all()
    return render_template("home.html", categories=categories)


@bp.route("/search")
def search():
    """Search results page.

    Query parameters:
        need (str): the category slug or free-text need
        open_now (str): "true" or absent — filter to services open right now

    Behaviour:
        - If `need` matches a category slug, returns all services in that
          category. Otherwise falls back to a substring match against
          category display names.
        - If `open_now=true`, services not open at the current moment are
          filtered out.
        - Inactive services (is_active=False) are always excluded from
          search results. They are still reachable by direct URL so the
          demo can show "this used to exist but doesn't any more" entries.
    """
    need = (request.args.get("need") or "").strip().lower()
    open_now = request.args.get("open_now") == "true"
    now = datetime.now()

    # Start with all active services. Filtering happens in Python because the
    # category match is fuzzy and is_open_at requires the relationship loaded.
    # For 13-50 services this is fine; if the directory grew to thousands it
    # would be worth pushing the category match into a SQL query.
    candidates = Service.query.filter_by(is_active=True).all()

    if need:
        candidates = [s for s in candidates if s.matches_need(need)]

    if open_now:
        candidates = [s for s in candidates if s.is_open_at(now)]

    # Sort: services explicitly open now first (most useful for Aisha), then
    # by name. Stable across calls.
    candidates.sort(key=lambda s: (not s.is_open_at(now), s.name.lower()))

    categories = Category.query.order_by(Category.display_name).all()
    return render_template(
        "search_results.html",
        services=candidates,
        need=need,
        open_now=open_now,
        now=now,
        categories=categories,
    )


@bp.route("/service/<int:service_id>")
def service_detail(service_id: int):
    """Full detail page for one service.

    Shows everything a resident needs to decide whether to visit:
    description, address, opening hours for the whole week, eligibility,
    languages spoken (when populated), and how the system knows about
    this service (provenance — supports the freshness/trust narrative
    of US-20).

    Inactive services are shown with a clear "this service is currently
    closed" banner so a user who arrives via an old link doesn't waste
    a trip.
    """
    service = Service.query.get(service_id)
    if service is None:
        abort(404)

    now = datetime.now()
    return render_template(
        "service_detail.html",
        service=service,
        now=now,
        is_open_now=service.is_open_at(now) if service.is_active else False,
    )
