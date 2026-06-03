"""
Ladywood Community Services Finder — Flask application factory.

This module exposes `create_app()`, which constructs and configures the Flask
application instance. Using the factory pattern (rather than a module-level
`app = Flask(__name__)`) keeps tests isolated and makes future configuration
changes straightforward.
"""

from flask import Flask


def create_app(config: dict | None = None) -> Flask:
    """Create and configure a Flask application instance.

    Args:
        config: Optional dict of configuration overrides. Useful for tests.

    Returns:
        A configured Flask application ready to run.
    """
    app = Flask(__name__)

    # Default configuration. Override via the `config` argument in tests
    # or via environment variables in deployment.
    app.config.from_mapping(
        SECRET_KEY="dev",  # replaced with a real secret in production
        SQLALCHEMY_DATABASE_URI="sqlite:///ladywood.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if config is not None:
        app.config.update(config)

    # Placeholder route so the app is runnable from day one.
    # Real routes will live in src/routes/ and be registered as blueprints.
    @app.route("/")
    def index() -> str:
        return "Ladywood Community Services Finder — under development."

    return app


# Allow `flask --app src.app run` to find an application instance.
app = create_app()
