"""
Integration tests for the admin routes.

Covers:
    US-13  Add a service
    US-15  Login with email + password
    US-16  Mark service as temporarily closed
    US-17  Save confirmation
"""

from __future__ import annotations

import pytest

from src.models import OrgAdmin, Service, db


@pytest.fixture
def admin_credentials():
    return {"email": "sarah@example.org", "password": "test-pw-123!"}


@pytest.fixture
def app_with_admin(app, admin_credentials):
    """An app with one OrgAdmin pre-created for login tests."""
    with app.app_context():
        admin = OrgAdmin(
            email=admin_credentials["email"],
            organisation_name="Test Org",
        )
        admin.set_password(admin_credentials["password"])
        db.session.add(admin)
        db.session.commit()
    yield app


# ----------------------------------------------------------------------------
# Login / logout
# ----------------------------------------------------------------------------


def test_login_page_returns_200(client):
    response = client.get("/admin/login")
    assert response.status_code == 200
    assert b"Email" in response.data
    assert b"Password" in response.data


def test_login_with_valid_credentials_redirects(app_with_admin, admin_credentials):
    client = app_with_admin.test_client()
    response = client.post(
        "/admin/login",
        data=admin_credentials,
        follow_redirects=False,
    )
    assert response.status_code == 302
    assert "/admin/services" in response.headers["Location"]


def test_login_with_wrong_password_fails(app_with_admin, admin_credentials):
    client = app_with_admin.test_client()
    response = client.post(
        "/admin/login",
        data={"email": admin_credentials["email"], "password": "wrong"},
    )
    assert response.status_code == 401
    assert b"not recognised" in response.data


def test_login_with_unknown_email_fails(app_with_admin):
    client = app_with_admin.test_client()
    response = client.post(
        "/admin/login",
        data={"email": "nobody@example.org", "password": "x"},
    )
    assert response.status_code == 401


def test_admin_pages_require_login(client):
    """All admin routes redirect to login when not authenticated."""
    for path in ("/admin/services", "/admin/services/new"):
        response = client.get(path, follow_redirects=False)
        assert response.status_code == 302
        assert "/admin/login" in response.headers["Location"]


def test_logout_clears_session(app_with_admin, admin_credentials):
    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)

    # Verify logged in
    r1 = client.get("/admin/services")
    assert r1.status_code == 200

    # Logout
    r2 = client.post("/admin/logout", follow_redirects=False)
    assert r2.status_code == 302

    # Now blocked again
    r3 = client.get("/admin/services", follow_redirects=False)
    assert r3.status_code == 302


# ----------------------------------------------------------------------------
# Service list / add / edit
# ----------------------------------------------------------------------------


def test_list_services_shows_existing(app_with_admin, admin_credentials):
    """The admin service list shows existing services."""
    with app_with_admin.app_context():
        s = Service(
            name="An Existing Service",
            description="x",
            address="x",
            is_active=True,
        )
        db.session.add(s)
        db.session.commit()

    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)
    response = client.get("/admin/services")
    assert response.status_code == 200
    assert b"An Existing Service" in response.data


def test_add_service_creates_a_new_one(app_with_admin, admin_credentials):
    """Posting the add-service form creates a new Service in the DB (US-13)."""
    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)

    response = client.post(
        "/admin/services/new",
        data={
            "name": "Brand New Service",
            "description": "A test service created via the admin UI.",
            "address": "1 Demo Lane",
            "postcode": "B1 1XX",
            "is_drop_in": "true",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Brand New Service" in response.data
    assert b"added" in response.data.lower()

    with app_with_admin.app_context():
        assert Service.query.filter_by(name="Brand New Service").first() is not None


def test_add_service_validates_required_fields(app_with_admin, admin_credentials):
    """Missing required fields returns the form again with an error (US-17)."""
    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)

    response = client.post(
        "/admin/services/new",
        data={
            "name": "",  # missing
            "description": "x",
            "address": "x",
        },
    )
    assert response.status_code == 400
    assert b"Please fill in" in response.data


def test_edit_service_updates_fields(app_with_admin, admin_credentials):
    """Editing a service persists the changes (US-14, US-17)."""
    with app_with_admin.app_context():
        s = Service(
            name="Old Name",
            description="Old description.",
            address="Old address",
            is_active=True,
        )
        db.session.add(s)
        db.session.commit()
        service_id = s.id

    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)

    response = client.post(
        f"/admin/services/{service_id}/edit",
        data={
            "name": "New Name",
            "description": "New description.",
            "address": "New address",
            "is_active": "true",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"New Name" in response.data

    with app_with_admin.app_context():
        updated = db.session.get(Service, service_id)
        assert updated.name == "New Name"
        assert updated.description == "New description."


def test_mark_service_temporarily_closed(app_with_admin, admin_credentials):
    """Unticking is_active on the edit form marks the service as closed (US-16)."""
    with app_with_admin.app_context():
        s = Service(
            name="To Be Closed",
            description="x",
            address="x",
            is_active=True,
        )
        db.session.add(s)
        db.session.commit()
        service_id = s.id

    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)

    # Submit form without is_active checkbox -> service goes inactive
    response = client.post(
        f"/admin/services/{service_id}/edit",
        data={
            "name": "To Be Closed",
            "description": "x",
            "address": "x",
            # 'is_active' deliberately omitted
        },
        follow_redirects=True,
    )
    assert response.status_code == 200

    with app_with_admin.app_context():
        updated = db.session.get(Service, service_id)
        assert updated.is_active is False

    # And the service no longer appears in resident search
    r = client.get("/search?need=&open_now=false")
    assert b"To Be Closed" not in r.data


def test_save_confirmation_appears_after_edit(app_with_admin, admin_credentials):
    """A flash message confirms saves (US-17)."""
    with app_with_admin.app_context():
        s = Service(
            name="ConfirmMe",
            description="x",
            address="x",
            is_active=True,
        )
        db.session.add(s)
        db.session.commit()
        service_id = s.id

    client = app_with_admin.test_client()
    client.post("/admin/login", data=admin_credentials)

    response = client.post(
        f"/admin/services/{service_id}/edit",
        data={
            "name": "ConfirmMe",
            "description": "x",
            "address": "x",
            "is_active": "true",
        },
        follow_redirects=True,
    )
    assert b"saved" in response.data.lower()
