"""
Shared pytest fixtures for the test suite.

Each test gets a fresh Flask app with an in-memory SQLite database and a
small fixed set of services so assertions are deterministic.

Fixtures provided:
    app             — Flask app, configured for testing
    client          — Flask test client (for HTTP-level tests)
    db_session      — SQLAlchemy session bound to the test app
    seeded_app      — app with sample data already loaded
"""

from __future__ import annotations

from datetime import time

import pytest

from src.app import create_app
from src.models import Category, OpeningHours, Service, db


@pytest.fixture
def app():
    """A Flask app configured for testing, with an in-memory SQLite database."""
    app = create_app(
        config={
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    yield app


@pytest.fixture
def client(app):
    """A Flask test client for making fake HTTP requests."""
    return app.test_client()


@pytest.fixture
def db_session(app):
    """A SQLAlchemy session bound to the test app, with all tables fresh."""
    with app.app_context():
        yield db.session


@pytest.fixture
def seeded_app(app):
    """An app pre-populated with a small fixed dataset for route tests."""
    with app.app_context():
        food = Category(slug="food", display_name="Food banks")
        warmth = Category(slug="warmth", display_name="Warm spaces")
        db.session.add_all([food, warmth])
        db.session.flush()

        # An active drop-in service open Mon-Fri 09:00-17:00
        s1 = Service(
            name="Test Food Bank",
            description="An open food bank used in tests.",
            address="1 Test Street",
            postcode="B1 1AA",
            is_drop_in=True,
            requires_voucher=False,
            requires_referral=False,
            is_active=True,
        )
        s1.categories.append(food)
        for day in ("monday", "tuesday", "wednesday", "thursday", "friday"):
            s1.opening_hours.append(
                OpeningHours(
                    day_of_week=day,
                    opens_at=time(9, 0),
                    closes_at=time(17, 0),
                    is_closed=False,
                )
            )
        for day in ("saturday", "sunday"):
            s1.opening_hours.append(
                OpeningHours(day_of_week=day, is_closed=True)
            )

        # An inactive (closed) service
        s2 = Service(
            name="Closed Service",
            description="A service that is currently closed.",
            address="2 Test Street",
            postcode="B1 1BB",
            is_drop_in=False,
            is_active=False,
        )
        s2.categories.append(warmth)

        # A voucher-required service, open Tue only
        s3 = Service(
            name="Voucher Bank",
            description="A voucher-required food bank.",
            address="3 Test Street",
            postcode="B1 1CC",
            is_drop_in=False,
            requires_voucher=True,
            requires_referral=True,
            is_active=True,
        )
        s3.categories.append(food)
        for day in ("monday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            s3.opening_hours.append(
                OpeningHours(day_of_week=day, is_closed=True)
            )
        s3.opening_hours.append(
            OpeningHours(
                day_of_week="tuesday",
                opens_at=time(10, 0),
                closes_at=time(14, 0),
                is_closed=False,
            )
        )

        db.session.add_all([s1, s2, s3])
        db.session.commit()

    yield app
