from .base import BaseEnum


class Status(BaseEnum):
    """Enum for order statuses."""
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    CANCELED = "CANCELED"
    TIMEOUT = "TIMEOUT"
    FINISHED = "FINISHED"
    BANNED = "BANNED"
