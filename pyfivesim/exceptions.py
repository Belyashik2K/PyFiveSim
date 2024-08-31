from typing import Optional


class FiveSimException(BaseException):
    """Base class for exceptions in this module."""
    pass


class FiveSimDetailedException(FiveSimException):
    """Exception with a detailed message."""

    def __init__(
            self,
            status_code: Optional[int] = None,
            data: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.data = data

    def __str__(self):
        message = f"Request failed with status code {self.status_code}"
        if self.data:
            message += f". {self.data.capitalize()}."
        return message