import asyncio

from pyfivesim import PyFiveSimAsync
from pyfivesim.exceptions import (
    FiveSimNotEnoughBalance,
    FiveSimInternalError,
    FiveSimUnknownError,
)
from pyfivesim.enums import (
    OrderAction,
    Status,
)


async def main():
    key = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTU1NDMyMjksImlhdCI6MTcyNDAwNzIyOSwicmF5IjoiMjBiMTZmNzExNjgxZThhZjcxNjA0YjI2N2E3MzNkOGEiLCJzdWIiOjE0ODA0ODZ9.Wx1ZNFZZ8iExu5vIIe3DZj4kg4htK046-LoRfpkxh_cNhCuPl0-4x4bRGwV_Vllp_YVxFVj6TsoLehMReSk7Ax9re6MR84EU_FB94khaKogahzwbrENqDyVyEi0osKWksMFsAp0S2bRpzjIRUyFo_gciJpWVikARJKPSRuxI9RITC9lXRxTzNUffWPReNh41yu6GELRLAEs80LVTxBHFSPQPP9YdDCXAiP0vIE4A4LJFyPh9yiPWm1SSC6iNcnrjZhhpeRI2tepSwazpxhoR4BmzBcG9w6276h2RBrgreBAmG3AkzZGhEtWL0lrkyGkD8IrBu2orVhaM-5DDi81Vsw"
    async with PyFiveSimAsync(api_key=key) as client:
        await client.get_order_info(order_id="12")


if __name__ == "__main__":
    asyncio.run(main())
