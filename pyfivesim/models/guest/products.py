from pydantic import (
    BaseModel,
    Field,
)


class Product(BaseModel):
    name: str = Field(...)
    category: str = Field(..., alias="Category")
    price: float = Field(..., alias="Price")
    quantity: int = Field(..., alias="Qty")