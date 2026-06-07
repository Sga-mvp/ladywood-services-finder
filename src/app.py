"""
Ladywood Community Services Finder — Flask application factory.

Exposes `create_app()`, which builds and configures the Flask app instance.
The factory pattern keeps tests isolated (each test gets a fresh app with an
in-memory database) and makes future configuration changes straightforward.

Wires up:
  - Flask-SQLAlchemy via the `db` instance from src/models.py
  - The data model classes (registered when models.py is imported)
  - A placeholder index route (real routes will be added as Blueprints under src/routes/)
"""

from __future__ import annotations

from flask import Flask

from src.models import db


def create_app(config: dict | None = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config: Optional dict of configuration overrides. Tests pass this to
            point the app at an in-memory database; production deployments
            would override via environment variables.

    Returns:
        A configured Flask application ready to run.
    """
    app = Flask(__name__)

    # Default configuration. Override via the `config` argument in tests
    # or via environment variables when deploying.
    app.config.from_mapping(
        SECRET_KEY="dev",  # would be loaded from env var in production
        SQLALCHEMY_DATABASE_URI="sqlite:///ladywood.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config is not None:
        app.config.update(config)

    # Initialise the database against this app instance. Importing models above
    # registered all model classes against `db`; init_app binds `db` to `app`.
    db.init_app(app)

    # Create tables on first run. For a prototype, db.create_all() is fine —
    # production would use Alembic migrations.
    with app.app_context():
        db.create_all()

    # Placeholder route. Real routes will live in src/routes/ and be registered
    # as Blueprints here. See US-04, US-05, US-13 for the routes to come.
    @app.route("/")
    def index() -> str:
        return "Ladywood Community Services Finder — under development."

    return app


# Allow `flask --app src.app run` to find an application instance.
app = create_app()
