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


class FiveSimInvalidAPIKey(FiveSimDetailedException):
    """Exception raised if the API key is invalid."""
    ...


class FiveSimOrderNotFound(FiveSimDetailedException):
    """Exception raised if the order is not found."""
    ...


class FiveSimNoFreePhones(FiveSimDetailedException):
    """Exception raised if there are no free numbers."""
    ...


class FiveSimNotEnoughBalance(FiveSimDetailedException):
    """Exception raised if there is not enough balance."""
    ...


class FiveSimNoEnoughRating(FiveSimDetailedException):
    """Exception raised if there is not enough rating."""
    ...


class FiveSimInvalidCountry(FiveSimDetailedException):
    """Exception raised if the request is invalid."""
    ...


class FiveSimInvalidProduct(FiveSimDetailedException):
    """Exception raised if the product is invalid."""
    ...


class FiveSimInvalidOperator(FiveSimDetailedException):
    """Exception raised if the operator is invalid."""
    ...


class FiveSimReuseNotPossible(FiveSimDetailedException):
    """Exception raised if reusing is not possible."""
    ...


class FiveSimInternalError(FiveSimDetailedException):
    """Exception raised if there is an internal error."""
    ...

class FiveSimUnknownError(FiveSimDetailedException):
    """Exception raised if there is an unknown error."""
    ...