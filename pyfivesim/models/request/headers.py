from pydantic import (
    BaseModel,
    Field,
)


class RequestHeaders(BaseModel):
    api_key: str = Field(..., alias="Authorization")
    content_type: str = Field("application/json", alias="Accept")
