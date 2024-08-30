from .base import BaseEnum


class Action(BaseEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class OrderAction(BaseEnum):
    FINISH = "finish"
    CANCEL = "cancel"
    BAN = "ban"
