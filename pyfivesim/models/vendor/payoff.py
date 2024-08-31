from pydantic import (
    BaseModel,
    Field,
)

from ...enums.vendor_withdraw import VendorWithdrawMethod, VendorWithdrawFee

class VendorWithdraw(BaseModel):
    receiver: str = Field(...)
    method: VendorWithdrawMethod = Field(...)
    amount: float = Field(..., ge=0)
    fee: VendorWithdrawFee = Field(...)
