from enum import Enum


class BaseEnum(str, Enum):
    def __str__(self) -> str:
        return self.value
