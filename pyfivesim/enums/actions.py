from .base import BaseEnum


class Action(BaseEnum):
    """Enum for actions with price limits."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class OrderAction(BaseEnum):
    """Enum for actions with orders."""
    FINISH = "finish"
    CANCEL = "cancel"
    BAN = "ban"
