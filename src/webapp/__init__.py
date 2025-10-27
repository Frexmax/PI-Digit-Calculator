"""File implementing flask web app configuration."""
from flask import Flask

from .celery_extension import celery_init_app
from .pi_home_page import pi_home_page
from .pi_result_page import pi_result_page


def create_app() -> Flask:
    """
    Configure flask web app.

    :return: flask web app
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "SECRET_KEY"  # noqa: S105
    app.config["CELERY"] = {"broker_url": "redis://localhost:6379", "result_backend": "redis://localhost:6379"}

    celery_init_app(app)

    app.register_blueprint(pi_home_page, url_prefix="/")
    app.register_blueprint(pi_result_page, url_prefix="/")

    return app

__all__ = ["create_app"]
