"""File implementing the logic for calculating the digits of pi."""
from decimal import Decimal, getcontext
import math
from typing import Any

from celery import shared_task

from .pi_calculator_constants import MAX_NUMBER_OF_DIGITS, MIN_NUMBER_OF_DIGITS
from .pi_calculator_errors import InvalidNumberOfDigitsError


@shared_task(bind=True)  # type: ignore[misc]
def get_digits_of_pi(self: Any, num_digits: int) -> dict[str, str | int]:
    """
    Calculate and return the specified number of digits of pi. Limited to 15 due to floating point size.

    :param self: the task instance
    :param num_digits: how many digits of pi to return
    :return: 'num_digits' digits of pi
    """
    getcontext().prec = num_digits + 10  # Increase precision to reduce rounding errors

    if num_digits <= MIN_NUMBER_OF_DIGITS:
        msg = "Variable 'num_digits' must be positive"
        raise InvalidNumberOfDigitsError(msg)

    if num_digits > MAX_NUMBER_OF_DIGITS:
        msg = f"Variable 'num_digits' must be less than {MAX_NUMBER_OF_DIGITS}"
        raise InvalidNumberOfDigitsError(msg)

    # number of terms (iterations) needed is around n / 14
    number_of_iterations = num_digits // 14 + 1

    total = Decimal(0)
    k = 0

    self.update_state(state="PROGRESS", meta={"current": 0, "total": number_of_iterations})

    # run the chudnovsky algorithm to calculate digits
    while k < number_of_iterations:
        total += chudnovsky_term(k)
        k += 1
        self.update_state(state="PROGRESS", meta={"current": k, "total": number_of_iterations})

    pi = (Decimal(426880) * Decimal(10005).sqrt()) / total
    pi_str = str(pi)[:1] if num_digits == 1 else str(pi)[:num_digits + 1]

    return {"result": pi_str, "current": k, "total": number_of_iterations}


def chudnovsky_term(k: int) -> Decimal:
    """
    Compute the k-th term in the Chudnovsky series.

    :param k: the index of the term to compute.
    :return: the computed value of the k-th term of the series.
    """
    numerator = Decimal(math.factorial(6 * k)) * (13591409 + 545140134 * k)
    denominator = Decimal(math.factorial(3 * k)) * (math.factorial(k) ** 3) * (Decimal(-640320) ** (3 * k))
    return numerator / denominator

