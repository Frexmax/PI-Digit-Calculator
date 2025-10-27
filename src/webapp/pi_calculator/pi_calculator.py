"""File implementing the logic for calculating the digits of pi."""
import math

from celery import shared_task
from pi_calculator.pi_calculator_constants import MAX_NUMBER_OF_DIGITS, MIN_NUMBER_OF_DIGITS
from pi_calculator.pi_calculator_errors import InvalidNumberOfDigitsError


@shared_task  # type: ignore[misc]
def get_digits_of_pi(num_digits: int) -> float:
    """
    Calculate and return the specified number of digits of pi. Limited to 15 due to floating point size.

    :param num_digits: how many digits of pi to return
    :return: 'num_digits' digits of pi
    """
    if num_digits <= MIN_NUMBER_OF_DIGITS:
        msg = "Variable 'num_digits' must be positive"
        raise InvalidNumberOfDigitsError(msg)

    if num_digits > MAX_NUMBER_OF_DIGITS:
        msg = "Variable 'num_digits' must be less than 15"
        raise InvalidNumberOfDigitsError(msg)

    # calculate the necessary number of iterations to accurately compute the needed number of digits of pi
    # 'digits_per_iterations' is the property of chudnovsky algorithm,
    #   where for each iteration 14 digits of accuracy is gained
    digits_per_iterations = 14
    iterations = math.ceil(num_digits / digits_per_iterations)

    # calculate the digits of pi
    pi_approximate = chudnovsky(iterations)

    # get the necessary number of digits - need +2 elements, because it includes the decimal point '.'
    pi_approximate_str = str(pi_approximate)
    pi_approximate_str = pi_approximate_str[0:num_digits+1]

    # if someone requested one digit, then there would be the decimal point at the end -> remove it
    if pi_approximate_str[-1] == ".":
        pi_approximate_str = pi_approximate_str[:-1]

    return float(pi_approximate_str)


def chudnovsky(iterations: int) -> float:
    """
    Implement the chudnovsky algorithm to calculate the digits of pi.

    :param iterations: number of iterations to run the algorithm for
    :return: the approximation of pi
    """
    c = 426880 * math.sqrt(10005)

    pi_sum = 0
    for q in range(iterations):
        mq = math.factorial(6 * q) / (math.factorial(3 * q) * math.factorial(q) ** 3)
        lq = 545140 * q + 13591409
        xq = (-262537412640768000) ** q
        pi_sum += (mq * lq) / xq

    return c * (1 / pi_sum)
