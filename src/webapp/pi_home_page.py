"""TODO."""
from flask import Blueprint, Response, redirect, render_template, request, url_for

pi_home_page = Blueprint("home", __name__)


@pi_home_page.route("", methods=["GET", "POST"])
def home() -> str | Response:
    """TODO."""
    if request.method == "POST":
        # TODO: Do input verification!
        n = int(request.form["digit_input"])
        return redirect(url_for("pi_result_page.result_page", n=n))  # type: ignore[return-value]

    return render_template("pi_home_page.html")
