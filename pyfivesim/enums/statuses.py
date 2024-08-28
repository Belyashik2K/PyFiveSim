from enum import Enum


class Status(str, Enum):
    PENDING = "PENDING"
    RECEIVED = "RECEIVED"
    CANCELED = "CANCELED"
    TIMEOUT = "TIMEOUT"
    FINISHED = "FINISHED"
    BANNED = "BANNED"
