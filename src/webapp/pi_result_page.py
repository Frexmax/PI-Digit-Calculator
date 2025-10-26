"""TODO."""
from flask import Blueprint, render_template, request

from src.pi_calculator.pi_calculator import get_digits_of_pi

pi_result_page = Blueprint("pi_result_page", __name__)


@pi_result_page.route("calculate_pi", methods=["GET"])
def result_page() -> str:
    """TODO."""

    # TODO ADD VERIFY num_digits

    num_digits = int(request.args.get("n"))  # type: ignore[arg-type]
    result = str(get_digits_of_pi(num_digits))

    return render_template("result_page.html", num_digits=num_digits, result=result)
