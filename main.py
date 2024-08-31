import asyncio
import pprint
from http.client import responses

from pyfivesim import FiveSimAsync
from pyfivesim.clients.sync_client import FiveSimSync
from pyfivesim.enums import Category
from pyfivesim.enums.actions import (
    Action,
    OrderAction,
)
from pyfivesim.exceptions import FiveSimDetailedException


async def main() -> None:
    api_key = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTU1NDMyMjksImlhdCI6MTcyNDAwNzIyOSwicmF5IjoiMjBiMTZmNzExNjgxZThhZjcxNjA0YjI2N2E3MzNkOGEiLCJzdWIiOjE0ODA0ODZ9.Wx1ZNFZZ8iExu5vIIe3DZj4kg4htK046-LoRfpkxh_cNhCuPl0-4x4bRGwV_Vllp_YVxFVj6TsoLehMReSk7Ax9re6MR84EU_FB94khaKogahzwbrENqDyVyEi0osKWksMFsAp0S2bRpzjIRUyFo_gciJpWVikARJKPSRuxI9RITC9lXRxTzNUffWPReNh41yu6GELRLAEs80LVTxBHFSPQPP9YdDCXAiP0vIE4A4LJFyPh9yiPWm1SSC6iNcnrjZhhpeRI2tepSwazpxhoR4BmzBcG9w6276h2RBrgreBAmG3AkzZGhEtWL0lrkyGkD8IrBu2orVhaM-5DDi81Vsw"

    client = FiveSimSync(
        api_key=api_key
    )
    async_client = FiveSimAsync(
        api_key=api_key
    )

    profile = client.get_user_profile()
    print(profile)
    profile_async = await async_client.get_user_profile()
    print(profile_async)

    # products = client.get_prices(
    #     country="afghanistan",
    #     product="telegram"
    # )
    # print(products)

    # orders = client.get_user_orders(
    #     category=Category.activation,
    #     limit=5,
    #     offset=3,
    #     reverse=True
    # )
    # for order in orders.data:
    #     print(order)
    #
    # async_client = FiveSimAsync(
    #     api_key=api_key
    # )
    # profile = await async_client.get_user_profile()
    # print(profile)

if __name__ == "__main__":
    asyncio.run(main())
