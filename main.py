import asyncio
import pprint
from http.client import responses

from pyfivesim import FiveSimAsync
from pyfivesim.enums import Category
from pyfivesim.enums.actions import Action


async def main() -> None:
    client = FiveSimAsync(
        # api_key="eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTU1NDMyMjksImlhdCI6MTcyNDAwNzIyOSwicmF5IjoiMjBiMTZmNzExNjgxZThhZjcxNjA0YjI2N2E3MzNkOGEiLCJzdWIiOjE0ODA0ODZ9.Wx1ZNFZZ8iExu5vIIe3DZj4kg4htK046-LoRfpkxh_cNhCuPl0-4x4bRGwV_Vllp_YVxFVj6TsoLehMReSk7Ax9re6MR84EU_FB94khaKogahzwbrENqDyVyEi0osKWksMFsAp0S2bRpzjIRUyFo_gciJpWVikARJKPSRuxI9RITC9lXRxTzNUffWPReNh41yu6GELRLAEs80LVTxBHFSPQPP9YdDCXAiP0vIE4A4LJFyPh9yiPWm1SSC6iNcnrjZhhpeRI2tepSwazpxhoR4BmzBcG9w6276h2RBrgreBAmG3AkzZGhEtWL0lrkyGkD8IrBu2orVhaM-5DDi81Vsw"
    )
    response = await client.get_user_profile()
    print(response)
    # response = await client.get_user_orders(Category.activation,
    #                                         limit=5,
    #                                         offset=3,
    #                                         reverse=True)
    # if isinstance(response.data, list):
    #     for order in response.data:
    #         print(order)
    # response = await client.get_user_payments(
    #     limit=1,
    # )
    # print(response)
    # response = await client.get_user_price_limits()
    # for price_limit in response:
    #     print(price_limit)
    # request_model = ActionWithUserPriceLimit(
    #     action=Action.UPDATE,
    #     product_name="telegram",
    #     price=1
    # )
    # response = await client.action_with_user_price_limits(
    #     action=Action.CREATE,
    #     product_name="telegram",
    # )
    # print(response)
    # response = await client.get_countries_list()
    # for country in response:
    #     print(country)
    # response = await client.get_available_products(
    #         country="afghanistan",
    #         operator="any",
    #     )
    # for product in response:
    #     print("Product {} with price {}".format(product.name, product.price))
    #
    # response = await client.get_prices(
    #     country="afghanistan"
    # )
    # print(response)
    # for country in response.countries:
    #     print("Страна: {}".format(country.name))
    #     for operator in country.operators:
    #         print("Оператор: {}".format(operator.name))
    #         print("Цена: {}".format(operator.operator_info.price))
    # print(response)
    # if isinstance(response, list):
    #     for country in response:
    #         print(country.name)
    #         for product in country.products:
    #             print(product.name)
    #             for operator in product.operators:
    #                 print(operator.name)
    #                 print(operator.price)
    #             print()
    #         break
    # else:
    # pprint.pprint(response)

    data = await client.get_prices(country="afghanistan")
    data2 = await client.get_prices(product="telegram")
    data3 = await client.get_prices(country="afghanistan", product="telegram")
    data4 = await client.get_prices()

if __name__ == "__main__":
    asyncio.run(main())
