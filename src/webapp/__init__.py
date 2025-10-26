"""File implementing flask web app configuration."""
from flask import Flask

from .pi_home_page import pi_home_page
from .pi_result_page import pi_result_page


def create_app() -> Flask:
    """
    Configure flask web app.

    :return: flask web app
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SECRET_KEY"  # noqa: S105

    app.register_blueprint(pi_home_page, url_prefix="/")
    app.register_blueprint(pi_result_page, url_prefix="/")

    return app
