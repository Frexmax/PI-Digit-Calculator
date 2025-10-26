"""File implementing flask web app configuration."""
from flask import Flask


def create_app() -> Flask:
    """
    Configure flask web app.

    :return: flask web app
    """
    from .calculate_pi_page import calculate_pi_page

    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SECRET_KEY"  # noqa: S105

    app.register_blueprint(calculate_pi_page, url_prefix="/")

    return app
