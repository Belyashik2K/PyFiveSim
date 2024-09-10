from typing import (
    Optional,
    Any,
    Union,
)
from datetime import datetime

from pydantic import (
    BaseModel,
    Field,
    field_validator,
)

from ...enums import Status


class OrderSMS(BaseModel):
    code: str = Field(...)
    created_at: datetime = Field(...)
    date: datetime = Field(...)
    sender: str = Field(...)
    text: str = Field(...)


class Order(BaseModel):
    country: str = Field(...)
    created_at: datetime = Field(...)
    expires_at: datetime = Field(..., alias="expires")
    id: int = Field(...)
    operator: str = Field(...)
    phone: str = Field(...)
    product: str = Field(...)
    sms: Union[OrderSMS, list[OrderSMS], None] = Field(...)
    status: Status = Field(...)
    price: float = Field(...)

    # noinspection PyNestedDecorators
    @field_validator("sms", mode="before")
    @classmethod
    def validate_sms(cls, value: list) -> Optional[OrderSMS]:
        if value:
            return OrderSMS(**value[0]) if len(value) == 1 else [OrderSMS(**sms) for sms in value]
        return None


class UserOrders(BaseModel):
    data: Union[list[Order], Order, None] = Field(..., alias="Data")
    product_names: Optional[list[Any]] = Field(None, alias="ProductNames")
    statuses: Optional[list[Any]] = Field(None, alias="Statuses")
    total: int = Field(..., alias="Total", ge=0)

    # noinspection PyNestedDecorators
    @field_validator("data", mode="before")
    @classmethod
    def validate_data(cls, value: list) -> Union[list[Order], Order, None]:
        if not value:
            return None
        if len(value) == 1:
            return Order(**value[0])
        return [Order(**order) for order in value]

    # noinspection PyNestedDecorators
    @field_validator("product_names", "statuses", mode="before")
    @classmethod
    def validate_fields(cls, value: list) -> Optional[list[Any]]:
        return value or None
