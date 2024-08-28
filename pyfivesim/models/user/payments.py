from datetime import datetime
from typing import (
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)


class Payment(BaseModel):
    id: int = Field(..., alias="ID")
    amount: float = Field(..., alias="Amount")
    balance: float = Field(..., alias="Balance", ge=0)
    created_at: datetime = Field(..., alias="CreatedAt")
    provider: str = Field(..., alias="ProviderName")
    type: str = Field(..., alias="TypeName")


class PaymentProvider(BaseModel):
    name: str = Field(..., alias="Name")


class PaymentType(BaseModel):
    name: str = Field(..., alias="Name")


class UserPayments(BaseModel):
    data: Union[list[Payment], Payment, None] = Field(..., alias="Data")
    providers: Optional[list[PaymentProvider]] = Field(..., alias="PaymentProviders")
    types: Optional[list[PaymentType]] = Field(..., alias="PaymentTypes")
    total: int = Field(..., alias="Total", ge=0)

    # noinspection PyNestedDecorators
    @field_validator("data", mode="before")
    @classmethod
    def validate_data(cls, value: list) -> Union[list[Payment], Payment, None]:
        if not value:
            return None
        if len(value) == 1:
            return Payment(**value[0])
        return [Payment(**payment) for payment in value]

    # noinspection PyNestedDecorators
    @field_validator("providers", "types", mode="before")
    @classmethod
    def validate_fields(cls, value: list) -> list:
        return value or None
