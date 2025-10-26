"""File implementing the result endpoint of the pi calculator."""
from flask import Blueprint, render_template, request

from src.pi_calculator.pi_calculator import get_digits_of_pi

pi_result_page = Blueprint("pi_result_page", __name__)


@pi_result_page.route("calculate_pi", methods=["GET"])
def result_page() -> str:
    """
    Handle "GET" requests in the '/calculate_pi' endpoint of the pi calculator. Takes integer 'n' url parameter.

    :return: the result html page with number of digits to display and the calculated result as parameters
    """
    num_digits = int(request.args.get("n"))  # type: ignore[arg-type]
    pi_result = get_digits_of_pi(num_digits)
    if num_digits == 1:
        pi_result = int(pi_result)
    out_text = str(pi_result)
    return render_template("result_page.html", num_digits=num_digits, result=out_text)
