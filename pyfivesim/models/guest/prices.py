from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


class Price(BaseModel):
    price: float = Field(..., alias="cost")
    quantity: int = Field(..., alias="count")
    rate: Optional[float] = Field(..., ge=0)

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def validate_rate(cls, data: dict) -> dict:
        data["rate"] = data.get("rate", 0)
        return data

class OperatorWithPrice(BaseModel):
    name: str = Field(...)
    operator_info: Price = Field(...)

class ProductWithOperators(BaseModel):
    name: str = Field(...)
    operators: Optional[list[OperatorWithPrice]] = Field(...)

class CountryWithProducts(BaseModel):
    name: str = Field(...)
    products: Optional[list[ProductWithOperators]] = Field(...)

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def validate_operators(cls, data: dict) -> dict:
        from pyfivesim.utils.validators import validate_operators_in_model
        data = validate_operators_in_model(data, "products")
        return data

class ProductWithCountries(BaseModel):
    name: str = Field(...)
    countries: Optional[list[ProductWithOperators]] = Field(...)

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def validate_countries(cls, data: dict) -> dict:
        from pyfivesim.utils.validators import validate_operators_in_model
        data = validate_operators_in_model(data, "countries")
        return data
