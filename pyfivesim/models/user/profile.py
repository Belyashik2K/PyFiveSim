from typing import (
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator,
)


class DefaultCountry(BaseModel):
    name: str = Field(...)
    iso: str = Field(...)
    prefix: str = Field(...)


class DefaultOperator(BaseModel):
    name: Optional[str] = Field()

    # noinspection PyNestedDecorators
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, v):
        return v or None


class ProfileOrder(BaseModel):
    country: str = Field(...)
    service: str = Field(...)
    operator: str = Field(...)
    service_id: int = Field(...)  # No information about this field in the FiveSim API documentation
    price: float = Field(..., ge=0)


class UserProfile(BaseModel):
    id: int = Field(...)
    email: EmailStr = Field(...)
    balance: float = Field(..., ge=0)
    rating: float = Field(..., ge=0, le=96)
    default_country: DefaultCountry = Field(...)
    default_operator: DefaultOperator = Field(...)
    frozen_balance: float = Field(..., ge=0)
    did_order: bool = Field(...)
    last_order: ProfileOrder = Field(...)
    last_top_orders: list[ProfileOrder] = Field(...)
    last_top_idx: int = Field(...)
    total_active_orders: int = Field(..., ge=0)

    # noinspection PyNestedDecorators
    @field_validator("last_order", mode="before")
    @classmethod
    def validate_last_order(cls, value: str) -> ProfileOrder:
        prepared = value.split(":")
        return cls.get_order_model(prepared)

    # noinspection PyNestedDecorators
    @field_validator("last_top_orders", mode="before")
    @classmethod
    def validate_last_top_orders(cls, value: str) -> list[ProfileOrder]:
        prepared = [x.split(":") for x in value[1:-1].split(",")]
        return [
            cls.get_order_model(x) for x in prepared
        ]

    @classmethod
    def get_order_model(cls, data: list) -> ProfileOrder:
        return ProfileOrder(
            country=data[0],
            service=data[1],
            operator=data[2],
            service_id=data[3],
            price=data[4]
        )
