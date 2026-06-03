"""
Smoke tests — does the app boot, and does it respond to a basic request?

These run on every commit via GitHub Actions. They are deliberately minimal:
they will be supplemented (and eventually surpassed) by feature tests as
real routes and logic are added.
"""


def test_app_factory_returns_an_app(app):
    """The app factory should return a Flask app object."""
    assert app is not None
    assert app.config["TESTING"] is True


def test_index_route_responds(client):
    """The placeholder index route should return HTTP 200."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Ladywood" in response.data
