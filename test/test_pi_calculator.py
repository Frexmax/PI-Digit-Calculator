# ruff: noqa: PLR2004

"""File implementing tests for pi digit calculation logic."""
from pathlib import Path
import sys

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent) + "/src")

import pytest

from webapp.pi_calculator import InvalidNumberOfDigitsError, get_digits_of_pi


def test_get_digits_of_pi_invalid_number_of_digits() -> None:
    """Test the input verification in the 'get_digits_of_pi' method."""
    with pytest.raises(InvalidNumberOfDigitsError) as excinfo:
        get_digits_of_pi(0)
    assert "Variable 'num_digits' must be positive" in str(excinfo.value)

    with pytest.raises(InvalidNumberOfDigitsError) as excinfo:
        get_digits_of_pi(-1)
    assert "Variable 'num_digits' must be positive" in str(excinfo.value)

    with pytest.raises(InvalidNumberOfDigitsError) as excinfo:
        get_digits_of_pi(15)
    assert "Variable 'num_digits' must be less than 15" in str(excinfo.value)

    with pytest.raises(InvalidNumberOfDigitsError) as excinfo:
        get_digits_of_pi(100)
    assert "Variable 'num_digits' must be less than 15" in str(excinfo.value)


def test_valid_get_digits_of_pi() -> None:
    """Test the correct calculation for the digits of pi by the 'get_digits_of_pi' method."""
    pi = get_digits_of_pi(1)
    assert pi == 3

    pi = get_digits_of_pi(3)
    assert pi == 3.14

    pi = get_digits_of_pi(10)
    assert pi == 3.141592653

    pi = get_digits_of_pi(14)
    assert pi == 3.1415926535897
