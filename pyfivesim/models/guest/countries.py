from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)


class Country(BaseModel):
    name: str = Field(...)
    iso: str = Field(...)
    prefix: str = Field(...)
    text_en: str = Field(...)
    text_ru: str = Field(...)
    available_operators: list[str] = Field(...)

    # noinspection PyNestedDecorators
    @field_validator("iso", "prefix", mode="before")
    @classmethod
    def validate_fields(cls, value: dict) -> str:
        return list(value.keys())[0]

    # noinspection PyNestedDecorators
    @model_validator(mode="before")
    @classmethod
    def validate_operators(cls, data: dict) -> dict:
        operators = [operator for operator, _ in list(data.items())[4:-1]]
        data["available_operators"] = operators
        return data
