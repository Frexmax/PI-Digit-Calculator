"""TODO."""
from flask import Blueprint, render_template

calculate_pi_page = Blueprint("calculate_pi_page", __name__)

@calculate_pi_page.route("/", methods=["GET", "POST"])
def home() -> str:
    """TODO."""
    return render_template("calculate_pi_page.html")
