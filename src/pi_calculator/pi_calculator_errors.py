"""File implementing various errors related to pi calculations."""


class InvalidNumberOfDigitsError(Exception):
    """Class implementing an exception for pi calculator when the user provides an invalid number of digits."""

    def __init__(self, message: str) -> None:
        """
        Construct the exception with the provided message.

        :param message: message to display with the exception
        """
        self.message = message
        super().__init__(self.message)
