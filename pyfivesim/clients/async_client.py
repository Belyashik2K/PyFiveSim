import pprint
from typing import (
    Optional,
    Union,
    overload,
)
from pydantic import PositiveInt

from .base import FiveSimBaseClient
from .request.aiohttp import AiohttpRequestClient
from ..enums.actions import Action

from ..enums.request.connection import Connection
from ..enums.request.method import Method
from ..enums import Category
from ..models.guest.countries import Country
from ..models.guest.prices import (
    CountryWithProducts,
    OperatorWithPrice,
    Price,
    ProductWithCountries,
)
from ..models.guest.products import Product
from ..models.request.headers import RequestHeaders
from ..models.user import (
    UserProfile,
    UserOrders,
    UserPayments,
    UserPriceLimit,
)
from ..models.user.price_limits import UserPricePostDTO
from ..utils.generators import generate_full_link
from ..utils.validators import validate_api_key


class FiveSimAsync(FiveSimBaseClient, AiohttpRequestClient):
    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None
    ) -> None:
        self.__base_url = base_url or Connection.base_url.value
        self._api_key = api_key or None
        self._headers = RequestHeaders(
            Authorization=f"Bearer {api_key}"
        )
        super().__init__(
            headers=self._headers.model_dump(by_alias=True)
        )

    @validate_api_key
    async def get_user_profile(self) -> UserProfile:
        url = generate_full_link(self.__base_url, "user/profile")
        response = await self.request(Method.GET, url)
        return UserProfile(**response)

    @validate_api_key
    async def get_user_orders(
            self,
            category: Union[str, Category],
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserOrders:
        url = generate_full_link(
            self.__base_url,
            "user/orders",
            category=category.value if isinstance(category, Category) else category,
            limit=limit,
            offset=offset,
            order=order,
            reverse="true" if reverse else "false"
        )
        response = await self.request(Method.GET, url)
        return UserOrders(**response)

    @validate_api_key
    async def get_user_payments(
            self,
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserPayments:
        url = generate_full_link(
            self.__base_url,
            "user/payments",
            limit=limit,
            offset=offset,
            order=order,
            reverse="true" if reverse else "false"
        )
        response = await self.request(Method.GET, url)
        return UserPayments(**response)

    @validate_api_key
    async def get_user_price_limits(self) -> list[UserPriceLimit]:
        url = generate_full_link(self.__base_url, "user/max-prices")
        response = await self.request(Method.GET, url)
        return [UserPriceLimit(**limit) for limit in response]

    @validate_api_key
    async def action_with_user_price_limits(
            self,
            action: Action,
            product_name: str,
            price: Optional[float] = None
    ) -> bool:
        if action != Action.DELETE and price is None:
            raise ValueError("Price is required for action UPDATE or CREATE")

        url = generate_full_link(self.__base_url, "user/max-prices")
        method = Method.DELETE if action == Action.DELETE else Method.POST
        data = UserPricePostDTO(
            product_name=product_name,
            price=price
        )
        await self.request(
            method,
            url,
            json=data.model_dump(exclude_none=True),
            no_return=True
        )
        return True

    async def get_countries_list(self) -> list[Country]:
        url = generate_full_link(self.__base_url, "guest/countries")
        response = await self.request(Method.GET, url)
        return [Country(**info, name=country) for country, info in response.items()]

    async def get_available_products(
            self,
            country: str,
            operator: str
    ) -> list[Product]:
        url = generate_full_link(
            self.__base_url,
            f"guest/products/{country}/{operator}",
        )
        response = await self.request(Method.GET, url)
        return [Product(**data, name=name) for name, data in response.items()]

    @overload
    async def get_prices(self, country: str) -> CountryWithProducts:
        ...

    @overload
    async def get_prices(self, country: str, product: str) -> list[OperatorWithPrice]:
        ...

    @overload
    async def get_prices(self, product: str) -> ProductWithCountries:
        ...

    @overload
    async def get_prices(self) -> list[CountryWithProducts]:
        ...

    async def get_prices(
            self,
            country: Optional[str] = None,
            product: Optional[str] = None,
    ) -> CountryWithProducts | list[OperatorWithPrice] | ProductWithCountries | list[CountryWithProducts]:
        url = generate_full_link(
            self.__base_url,
            "guest/prices",
            country=country,
            product=product
        )
        response = await self.request(Method.GET, url)

        if country and not product:
            name, data = response.popitem()
            return CountryWithProducts(**data, name=country)
        if country and product:
            return [OperatorWithPrice(name=name, price=Price(**data)) for name, data in
                    response[country][product].items()]
        if not country and product:
            name, data = response.popitem()
            return ProductWithCountries(**data, name=name)
        return [CountryWithProducts(**data, name=country) for country, data in response.items()]
