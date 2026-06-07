"""
SQLAlchemy data model for the Ladywood Community Services Finder.

The classes in this module mirror the UML class diagram at
docs/uml/class.png. Every entity in the diagram is a class here; every
relationship in the diagram is expressed as a SQLAlchemy `relationship`.

Five entities (matching the diagram):

    - Service          — a community service
    - OpeningHours     — owned by Service (composition, 1 to 0..*)
    - Category         — a tag like 'food' or 'warmth'
    - ServiceCategory  — join table for the many-to-many between Service and Category
    - OrgAdmin         — a voluntary-sector coordinator who owns Services

When changing this file, update the class diagram first. The diagram is the
source of truth; this file is its implementation. Keeping them in sync is what
the Maintainability mark depends on.
"""

from __future__ import annotations

from datetime import date, datetime, time
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# Single SQLAlchemy instance. Initialised against an app in src/app.py via db.init_app(app).
# Models import this and inherit from db.Model.
db = SQLAlchemy()


# Bank holidays in scope for the prototype. Populate with real UK bank holiday
# dates as needed. Empty set means "no bank-holiday special handling yet" —
# Service.is_open_at() will fall through to the normal opening-hours check.
# TODO (post-v1): load these from gov.uk's bank holiday JSON feed at startup.
BANK_HOLIDAYS: set[date] = set()


# Weekday names used in OpeningHours.day_of_week. Mirrors the seed data JSON
# and matches Python's `datetime.strftime("%A").lower()` output.
WEEKDAY_NAMES = (
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
)


class Service(db.Model):
    """A community service that residents can search for and visit.

    Mirrors the `Service` class in the class diagram. Composition with
    OpeningHours (a service owns its hours), many-to-many with Category via
    ServiceCategory, owned by an OrgAdmin.
    """

    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(280), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    postcode = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    website = db.Column(db.String(300), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    requires_voucher = db.Column(db.Boolean, nullable=False, default=False)
    requires_referral = db.Column(db.Boolean, nullable=False, default=False)
    is_drop_in = db.Column(db.Boolean, nullable=False, default=True)

    eligibility_notes = db.Column(db.Text, nullable=True)

    # is_active distinguishes "currently running" from "in our directory but closed".
    # Closed services are kept (not deleted) so demos and historical records remain accurate.
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    # Provenance / audit fields. Useful both for the org-admin "last edited" display
    # (US-20) and for honest reporting of data freshness.
    data_sourced_from = db.Column(db.String(500), nullable=True)
    needs_verification = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Foreign key to OrgAdmin. Nullable because seed data services don't belong to
    # any admin — they were loaded by a script, not added through the admin UI.
    owner_id = db.Column(db.Integer, db.ForeignKey("org_admins.id"), nullable=True)

    # Relationships -----------------------------------------------------------

    # Composition: Service owns its OpeningHours. cascade="all, delete-orphan"
    # means deleting a Service deletes its hours; orphaned hours are deleted too.
    # This implements the filled-diamond relationship in the class diagram.
    opening_hours = db.relationship(
        "OpeningHours",
        back_populates="service",
        cascade="all, delete-orphan",
        order_by="OpeningHours.day_of_week",
    )

    # Many-to-many with Category via ServiceCategory.
    categories = db.relationship(
        "Category",
        secondary="service_categories",
        back_populates="services",
    )

    # Many-to-one with OrgAdmin.
    owner = db.relationship("OrgAdmin", back_populates="services")

    # Methods (as shown in the class diagram) ---------------------------------

    def is_open_at(self, when: datetime) -> bool:
        """Is this service open at the given datetime?

        Implements the activity diagram at docs/uml/activity.png exactly:

            1. Get day-of-week and time from `when`.
            2. If `when.date()` is a bank holiday AND the service has no
               bank-holiday hours defined: return False.
               (Bank-holiday hours are a future enhancement; for now any
               bank holiday returns False unless the service is in a
               24/7 category like a public outdoor space.)
            3. Look up opening hours for that day of week.
            4. If no hours exist for that day, or is_closed=True, or hours
               are unknown (opens_at/closes_at are None): return False.
            5. If `when.time()` falls between opens_at and closes_at: return True.
            6. Otherwise return False.

        A closed service (is_active=False) always returns False.
        """
        # Closed services are never open.
        if not self.is_active:
            return False

        target_date = when.date()
        target_time = when.time()

        # Bank-holiday branch. The activity diagram allows for "service has
        # bank-holiday hours defined" — not modelled in v1, so we conservatively
        # return False on any bank holiday.
        if target_date in BANK_HOLIDAYS:
            return False

        # Look up opening hours for the target day of the week.
        day_name = WEEKDAY_NAMES[when.weekday()]
        hours = next(
            (h for h in self.opening_hours if h.day_of_week == day_name),
            None,
        )

        if hours is None:
            return False

        return hours.covers(target_time)

    def matches_need(self, need: str) -> bool:
        """Does this service match a stated need?

        Used by the search route (US-05). A "need" is a category slug or
        free-text query. Matching is intentionally simple — exact category
        slug, or substring of a category display name. The route layer
        handles fallback to a "no matches" view.
        """
        if not need:
            return False
        need_lower = need.lower().strip()
        for category in self.categories:
            if (
                category.slug == need_lower
                or need_lower in category.slug
                or need_lower in category.display_name.lower()
            ):
                return True
        return False

    def __repr__(self) -> str:
        return f"<Service {self.id}: {self.name}>"


class OpeningHours(db.Model):
    """A single day's opening hours for a service.

    Mirrors the `OpeningHours` class in the class diagram. Composition target
    of Service (a row here cannot exist without a service).
    """

    __tablename__ = "opening_hours"

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(
        db.Integer, db.ForeignKey("services.id"), nullable=False, index=True
    )

    # Stored as a lowercase string ("monday", "tuesday", ...) so the seed JSON
    # and the database match without conversion. The class diagram used `int`
    # with 0=Monday; strings are more readable and the cost is one comparison.
    day_of_week = db.Column(db.String(10), nullable=False)

    # Nullable because some seed entries have unknown hours (needs_verification).
    opens_at = db.Column(db.Time, nullable=True)
    closes_at = db.Column(db.Time, nullable=True)

    # Explicit closed flag. None means "we don't know"; True means "closed today";
    # False means "open during opens_at..closes_at".
    is_closed = db.Column(db.Boolean, nullable=True)

    service = db.relationship("Service", back_populates="opening_hours")

    def covers(self, when: time) -> bool:
        """Does this opening-hours row cover the given time?

        Returns False if the day is closed, if hours are unknown, or if the
        time falls outside the open window. Does not handle midnight rollover
        (a service that closes after midnight) — out of scope for v1; no real
        service in the seed data crosses midnight.
        """
        if self.is_closed is True or self.is_closed is None:
            return False
        if self.opens_at is None or self.closes_at is None:
            return False
        return self.opens_at <= when <= self.closes_at

    def __repr__(self) -> str:
        return f"<OpeningHours service={self.service_id} {self.day_of_week}>"


class Category(db.Model):
    """A tag describing a kind of need a service addresses.

    Mirrors the `Category` class in the class diagram. Pure lookup table —
    no methods. Many-to-many with Service via ServiceCategory.
    """

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(40), nullable=False, unique=True, index=True)
    display_name = db.Column(db.String(120), nullable=False)

    services = db.relationship(
        "Service",
        secondary="service_categories",
        back_populates="categories",
    )

    def __repr__(self) -> str:
        return f"<Category {self.slug}>"


class ServiceCategory(db.Model):
    """Join table for the many-to-many between Service and Category.

    Mirrors the `ServiceCategory` class in the class diagram. Represented as a
    full class (rather than a hidden association table) because the diagram
    shows it that way, and because it leaves room to add attributes here later
    (e.g. a "primary category" flag) without a migration that restructures the
    relationship.
    """

    __tablename__ = "service_categories"

    service_id = db.Column(
        db.Integer, db.ForeignKey("services.id"), primary_key=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), primary_key=True
    )


class OrgAdmin(db.Model):
    """A voluntary-sector coordinator (e.g. Sarah in personas.md).

    Mirrors the `OrgAdmin` class in the class diagram. Owns the Services
    they create or edit. Authenticates with email + password (hashed).
    """

    __tablename__ = "org_admins"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(300), nullable=False)
    organisation_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    services = db.relationship("Service", back_populates="owner")

    def set_password(self, plaintext: str) -> None:
        """Hash and store a new password. Use this instead of writing to
        `password_hash` directly."""
        self.password_hash = generate_password_hash(plaintext)

    def verify_password(self, plaintext: str) -> bool:
        """Check a plaintext password against the stored hash.

        Mirrors the `verify_password` method shown on the class diagram.
        Uses werkzeug's constant-time comparison to avoid timing attacks.
        """
        return check_password_hash(self.password_hash, plaintext)

    def __repr__(self) -> str:
        return f"<OrgAdmin {self.email}>"
