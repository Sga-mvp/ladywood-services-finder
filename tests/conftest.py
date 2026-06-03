"""
Shared pytest fixtures for the Ladywood Services Finder test suite.

Fixtures defined here are automatically available to every test file in
this directory and below. The `app` and `client` fixtures isolate each
test with an in-memory database so tests cannot interfere with each other
or with the dev database.
"""

import pytest

from src.app import create_app


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
    """A Flask test client for making fake HTTP requests in tests."""
    return app.test_client()
