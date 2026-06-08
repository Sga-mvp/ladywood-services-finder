"""
Unit tests for Service.is_open_at and OpeningHours.covers.

These tests are derived directly from the activity diagram at
docs/uml/activity.png. Every "Return False" path in the diagram is one
negative test; the single "Return True" path is one positive test. The
goal is full coverage of the branching logic, not the database.
"""

from __future__ import annotations

from datetime import date, datetime, time

import pytest

from src.models import (
    BANK_HOLIDAYS,
    Category,
    OpeningHours,
    Service,
    db,
)


# ----------------------------------------------------------------------------
# Service.is_open_at — covers the activity diagram branches
# ----------------------------------------------------------------------------


def _make_service(app, *, is_active=True, hours=None):
    """Helper: create and persist a service with given opening hours."""
    with app.app_context():
        s = Service(
            name="Helper Service",
            description="x",
            address="x",
            is_active=is_active,
        )
        for h in hours or []:
            s.opening_hours.append(h)
        db.session.add(s)
        db.session.commit()
        return s.id


def test_inactive_service_is_never_open(app):
    """An is_active=False service returns False even within its hours."""
    sid = _make_service(
        app,
        is_active=False,
        hours=[
            OpeningHours(
                day_of_week="monday",
                opens_at=time(9, 0),
                closes_at=time(17, 0),
                is_closed=False,
            )
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        # Monday 2026-06-08 at 10:00 — squarely inside opening hours
        assert s.is_open_at(datetime(2026, 6, 8, 10, 0)) is False


def test_bank_holiday_returns_false(app):
    """A date in BANK_HOLIDAYS returns False even if hours would otherwise cover."""
    # Inject a bank holiday for this test, restore after
    BANK_HOLIDAYS.add(date(2026, 12, 25))
    try:
        sid = _make_service(
            app,
            hours=[
                OpeningHours(
                    day_of_week="friday",  # 2026-12-25 was a Friday
                    opens_at=time(9, 0),
                    closes_at=time(17, 0),
                    is_closed=False,
                )
            ],
        )
        with app.app_context():
            s = db.session.get(Service, sid)
            assert s.is_open_at(datetime(2026, 12, 25, 10, 0)) is False
    finally:
        BANK_HOLIDAYS.discard(date(2026, 12, 25))


def test_no_hours_defined_for_day_returns_false(app):
    """A day with no OpeningHours row returns False."""
    sid = _make_service(
        app,
        hours=[
            OpeningHours(
                day_of_week="monday",
                opens_at=time(9, 0),
                closes_at=time(17, 0),
                is_closed=False,
            )
            # No tuesday entry at all
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        # 2026-06-09 was a Tuesday
        assert s.is_open_at(datetime(2026, 6, 9, 10, 0)) is False


def test_day_marked_closed_returns_false(app):
    """A day with is_closed=True returns False."""
    sid = _make_service(
        app,
        hours=[
            OpeningHours(day_of_week="monday", is_closed=True),
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        assert s.is_open_at(datetime(2026, 6, 8, 10, 0)) is False


def test_time_before_open_returns_false(app):
    """A time before opens_at returns False."""
    sid = _make_service(
        app,
        hours=[
            OpeningHours(
                day_of_week="monday",
                opens_at=time(9, 0),
                closes_at=time(17, 0),
                is_closed=False,
            ),
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        assert s.is_open_at(datetime(2026, 6, 8, 8, 30)) is False


def test_time_after_close_returns_false(app):
    """A time after closes_at returns False."""
    sid = _make_service(
        app,
        hours=[
            OpeningHours(
                day_of_week="monday",
                opens_at=time(9, 0),
                closes_at=time(17, 0),
                is_closed=False,
            ),
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        assert s.is_open_at(datetime(2026, 6, 8, 17, 30)) is False


def test_time_within_hours_returns_true(app):
    """The single positive path: active service, day has hours, time within them."""
    sid = _make_service(
        app,
        hours=[
            OpeningHours(
                day_of_week="monday",
                opens_at=time(9, 0),
                closes_at=time(17, 0),
                is_closed=False,
            ),
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        assert s.is_open_at(datetime(2026, 6, 8, 10, 0)) is True


def test_unknown_hours_returns_false(app):
    """Hours with opens_at=None (unknown) return False — better safe than wrong."""
    sid = _make_service(
        app,
        hours=[
            OpeningHours(
                day_of_week="monday",
                opens_at=None,
                closes_at=None,
                is_closed=None,
            ),
        ],
    )
    with app.app_context():
        s = db.session.get(Service, sid)
        assert s.is_open_at(datetime(2026, 6, 8, 10, 0)) is False


# ----------------------------------------------------------------------------
# OpeningHours.covers — small helper, but worth its own tests
# ----------------------------------------------------------------------------


def test_covers_true_in_range():
    h = OpeningHours(
        day_of_week="monday",
        opens_at=time(9, 0),
        closes_at=time(17, 0),
        is_closed=False,
    )
    assert h.covers(time(12, 0)) is True


def test_covers_false_when_closed_flag_true():
    h = OpeningHours(day_of_week="monday", is_closed=True)
    assert h.covers(time(12, 0)) is False


def test_covers_false_when_hours_unknown():
    h = OpeningHours(
        day_of_week="monday", opens_at=None, closes_at=None, is_closed=None
    )
    assert h.covers(time(12, 0)) is False


def test_covers_boundary_inclusive_at_open():
    """At exactly opens_at, covers should return True (we use inclusive ≤)."""
    h = OpeningHours(
        day_of_week="monday",
        opens_at=time(9, 0),
        closes_at=time(17, 0),
        is_closed=False,
    )
    assert h.covers(time(9, 0)) is True


def test_covers_boundary_inclusive_at_close():
    """At exactly closes_at, covers should return True (we use inclusive ≤)."""
    h = OpeningHours(
        day_of_week="monday",
        opens_at=time(9, 0),
        closes_at=time(17, 0),
        is_closed=False,
    )
    assert h.covers(time(17, 0)) is True


# ----------------------------------------------------------------------------
# Service.matches_need — the search-matching logic
# ----------------------------------------------------------------------------


def test_matches_need_exact_slug(app):
    with app.app_context():
        cat = Category(slug="food", display_name="Food banks")
        s = Service(name="x", description="x", address="x")
        s.categories.append(cat)
        db.session.add(s)
        db.session.commit()
        assert s.matches_need("food") is True


def test_matches_need_case_insensitive(app):
    with app.app_context():
        cat = Category(slug="food", display_name="Food banks")
        s = Service(name="x", description="x", address="x")
        s.categories.append(cat)
        db.session.add(s)
        db.session.commit()
        assert s.matches_need("FOOD") is True
        assert s.matches_need("  food  ") is True


def test_matches_need_substring_of_display_name(app):
    with app.app_context():
        cat = Category(slug="warmth", display_name="Warm spaces")
        s = Service(name="x", description="x", address="x")
        s.categories.append(cat)
        db.session.add(s)
        db.session.commit()
        assert s.matches_need("warm") is True


def test_matches_need_empty_string_returns_false(app):
    with app.app_context():
        cat = Category(slug="food", display_name="Food banks")
        s = Service(name="x", description="x", address="x")
        s.categories.append(cat)
        db.session.add(s)
        db.session.commit()
        assert s.matches_need("") is False


def test_matches_need_no_match_returns_false(app):
    with app.app_context():
        cat = Category(slug="food", display_name="Food banks")
        s = Service(name="x", description="x", address="x")
        s.categories.append(cat)
        db.session.add(s)
        db.session.commit()
        assert s.matches_need("electricity") is False
