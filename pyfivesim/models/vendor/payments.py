from typing import (
    Any,
    Optional,
)

from pydantic import (
    Field,
    field_validator,
)

from ..user.payments import UserPayments


class VendorPayments(UserPayments):
    statuses: Optional[list[Any]] = Field(..., alias="PaymentStatuses")

    # noinspection PyNestedDecorators
    @field_validator("statuses", mode="before")
    @classmethod
    def validate_fields(cls, value: list) -> list:
        return value or None