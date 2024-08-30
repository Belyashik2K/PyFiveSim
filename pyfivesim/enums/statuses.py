from .base import BaseEnum


class Status(BaseEnum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    CANCELED = "CANCELED"
    TIMEOUT = "TIMEOUT"
    FINISHED = "FINISHED"
    BANNED = "BANNED"
