from .base import BaseEnum


class VendorWithdrawMethod(BaseEnum):
    """Enum for vendor withdraw methods."""
    VISA = "visa"
    QIWI = "qiwi"
    YANDEX = "yandex"


class VendorWithdrawFee(BaseEnum):
    """Enum for vendor withdraw payment systems."""
    FKWALLET = "fkwallet"
    PAYEER = "payeer"
    UNITPAY = "unitpay"
