![5sim](https://github.com/user-attachments/assets/6e088361-a84a-46b6-8389-5b4f96cb0df5)

# PyFiveSim
> Sync/async Python wrapper for [5sim](https://5sim.biz/) API

## Installing

    pip install PyFiveSim

## Features
* Two available clients: sync (HTTPX) and async (AIOHTTP), which can be used as context managers or as instances
* Methods return Pydantic model as result for easier interaction with data
* Enums for prettier code
* Full exception handling
> Library documentation is already in development...

## Usage
```python
import asyncio

from pyfivesim import PyFiveSimAsync
from pyfivesim.exceptions import (
    FiveSimNotEnoughBalance,
    FiveSimUnknownError,
    FiveSimNoFreePhones,
)
from pyfivesim.enums import (
    OrderAction,
    Status,
)


async def main():
    api_key = "YOUR_API_KEY"
    
    # Create a client instance or use async with ...
    client = PyFiveSimAsync(
        api_key=api_key,
        base_url="https://5sim.net/v1" # Optional, default is "https://5sim.biz/v1",
    )
    # or use sync client PyFiveSimSync(api_key=api_key)
    
    # Get the user profile and print the ID, balance, and rating
    profile = await client.get_user_profile()
    print("ID >>>", profile.id)
    print("Balance >>>", profile.balance)
    print("Rating >>>", profile.rating)
    # Get last 5 user orders and print the service and price
    for order in profile.last_top_orders:
        print("Service >>>", order.service)
        print("Operator >>>", order.operator)
        print("Price >>>", order.price)

    # Try to buy a number
    try:
        order = await client.buy_number(
            product="youdo",
            country="russia",
            max_price=5,
        )
    except FiveSimNotEnoughBalance:
        print("O-o-p-s! Not enough balance :(")
    except FiveSimNoFreePhones:
        print("O-o-p-s! No free numbers :(")
    except FiveSimUnknownError as exc:
        print("Unknown error occurred :(")
        print("Error status code >>>", exc.status_code)
        print("Error message >>>", exc.data)
    else:
        print("W-o-o-h-o-o! Number bought successfully!")
        print("Phone number >>>", order.phone)
        print("Price >>>", order.price)

        print("Start checking for SMS...")
        sleep_for = 5
        while not order.status == Status.FINISHED:
            await asyncio.sleep(sleep_for)
            order = await client.get_order_info(order.id)
            if order.sms:
                print("SMS received! :)")
                print("SMS text >>>", order.sms.text)
                print("SMS code >>>", order.sms.code)
                print("Finish the order...")
                await client.action_with_order(OrderAction.FINISH, order.id)
                print("Order finished successfully!")
                break
            else:
                print(f"No SMS received yet, sleep for {sleep_for} seconds :(")


if __name__ == "__main__":
    asyncio.run(main())
```

## Docs
> Go to https://5sim.biz/ for more information about API methods

