from .base import BaseEnum


class VendorWithdrawMethod(BaseEnum):
    VISA = "visa"
    QIWI = "qiwi"
    YANDEX = "yandex"


class VendorWithdrawFee(BaseEnum):
    FKWALLET = "fkwallet"
    PAYEER = "payeer"
    UNITPAY = "unitpay"
