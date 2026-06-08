"""
Org-admin routes.

Implements the Must- and Should-have admin stories:

    US-13  Add a service              add_service
    US-15  Log in (email + password)  login
    US-16  Mark as temporarily closed edit_service (via is_active toggle)
    US-17  Save confirmation          flash messages on every save

All routes here require a logged-in admin except `login`. Authentication is
session-based: a successful login sets `session["admin_id"]`, and the
`login_required` decorator checks for it. Logout clears the session.

The form is intentionally lean (US-13 says "in under 5 minutes"). Opening
hours, language tagging, and category management are deferred to v2 — Sarah
can still mark a service as temporarily closed, which covers the most
time-sensitive update workflow (US-16).
"""

from __future__ import annotations

from functools import wraps
from typing import Callable

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.models import OrgAdmin, Service, db


bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(view: Callable) -> Callable:
    """Decorator that redirects anonymous users to the login page.

    Wrapped views can rely on `g_admin()` (below) to fetch the current admin.
    """

    @wraps(view)
    def wrapped(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please log in to access this page.", "info")
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


def current_admin() -> OrgAdmin | None:
    """Return the OrgAdmin for the current session, or None."""
    admin_id = session.get("admin_id")
    if admin_id is None:
        return None
    return db.session.get(OrgAdmin, admin_id)


# ----------------------------------------------------------------------------
# Authentication
# ----------------------------------------------------------------------------


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Show and process the login form."""
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        admin = OrgAdmin.query.filter_by(email=email).first()
        if admin is None or not admin.verify_password(password):
            # Deliberately vague error message — doesn't reveal which field
            # was wrong. Standard practice; deters credential stuffing.
            flash("Email or password not recognised.", "error")
            return render_template("admin/login.html", email=email), 401

        # Successful login.
        session.clear()
        session["admin_id"] = admin.id
        flash(f"Signed in as {admin.email}.", "success")

        next_url = request.args.get("next") or url_for("admin.list_services")
        return redirect(next_url)

    return render_template("admin/login.html", email="")


@bp.route("/logout", methods=["POST"])
def logout():
    """End the admin session.

    POST only — prevents accidental logout from a stray link click and
    avoids CSRF on logout via image-based attacks.
    """
    session.clear()
    flash("Signed out.", "info")
    return redirect(url_for("search.home"))


# ----------------------------------------------------------------------------
# Service management
# ----------------------------------------------------------------------------


@bp.route("/services")
@login_required
def list_services():
    """List the admin's services (and all services for now — v1 has one admin).

    In v2 this would filter by owner_id == current_admin().id.
    """
    services = Service.query.order_by(Service.name).all()
    return render_template(
        "admin/list_services.html", services=services, admin=current_admin()
    )


@bp.route("/services/new", methods=["GET", "POST"])
@login_required
def add_service():
    """Add a new service (US-13)."""
    if request.method == "POST":
        service = Service(
            name=(request.form.get("name") or "").strip(),
            description=(request.form.get("description") or "").strip(),
            address=(request.form.get("address") or "").strip(),
            postcode=(request.form.get("postcode") or "").strip() or None,
            requires_voucher=bool(request.form.get("requires_voucher")),
            requires_referral=bool(request.form.get("requires_referral")),
            is_drop_in=bool(request.form.get("is_drop_in")),
            eligibility_notes=(request.form.get("eligibility_notes") or "").strip() or None,
            is_active=True,
            owner_id=current_admin().id,
        )

        # Basic validation. Required fields are name, description, address.
        if not service.name or not service.description or not service.address:
            flash(
                "Please fill in the name, description, and address.", "error"
            )
            return render_template(
                "admin/edit_service.html",
                service=service,
                is_new=True,
            ), 400

        db.session.add(service)
        db.session.commit()

        flash(f'Service "{service.name}" added.', "success")
        return redirect(url_for("admin.list_services"))

    # GET: empty form.
    return render_template(
        "admin/edit_service.html",
        service=Service(is_active=True, is_drop_in=True),
        is_new=True,
    )


@bp.route("/services/<int:service_id>/edit", methods=["GET", "POST"])
@login_required
def edit_service(service_id: int):
    """Edit an existing service (US-14, US-16, US-17).

    The same form handles general edits and the "mark as temporarily closed"
    workflow — there is an `is_active` checkbox at the bottom that, when
    unticked, takes the service out of resident search results (US-16).
    """
    service = db.session.get(Service, service_id)
    if service is None:
        abort(404)

    if request.method == "POST":
        service.name = (request.form.get("name") or "").strip()
        service.description = (request.form.get("description") or "").strip()
        service.address = (request.form.get("address") or "").strip()
        service.postcode = (request.form.get("postcode") or "").strip() or None
        service.requires_voucher = bool(request.form.get("requires_voucher"))
        service.requires_referral = bool(request.form.get("requires_referral"))
        service.is_drop_in = bool(request.form.get("is_drop_in"))
        service.eligibility_notes = (
            request.form.get("eligibility_notes") or ""
        ).strip() or None
        service.is_active = bool(request.form.get("is_active"))

        if not service.name or not service.description or not service.address:
            flash(
                "Please fill in the name, description, and address.", "error"
            )
            return render_template(
                "admin/edit_service.html",
                service=service,
                is_new=False,
            ), 400

        db.session.commit()
        flash(f'Changes to "{service.name}" saved.', "success")
        return redirect(url_for("admin.list_services"))

    return render_template(
        "admin/edit_service.html",
        service=service,
        is_new=False,
    )
