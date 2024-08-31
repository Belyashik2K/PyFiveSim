from pydantic import BaseModel, Field

class VendorWallets(BaseModel):
    fkwallet: float = Field(..., ge=0)
    payeer: float = Field(..., ge=0)
    unitpay: float = Field(..., ge=0)

