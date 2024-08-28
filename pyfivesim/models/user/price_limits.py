from typing import (
    Union,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
)


class UserPricePostDTO(BaseModel):
    product_name: str = Field(...)
    price: Optional[float] = Field(..., ge=0)


class UserPriceLimit(BaseModel):
    id: int = Field(...)
    product: str = Field(...)
    price: float = Field(..., ge=0)
    created_at: str = Field(...)
