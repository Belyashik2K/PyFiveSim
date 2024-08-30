import pprint
from typing import (
    Optional,
    Union,
    overload,
    Literal,
)
from pydantic import PositiveInt

from .base import FiveSimBaseClient
from .request.aiohttp import AiohttpRequestClient
from ..enums.actions import (
    Action,
    OrderAction,
)
from ..enums.langs import Lang

from ..enums.request.connection import Connection
from ..enums.request.method import Method
from ..enums import (
    Category,
    BaseValue,
)
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
from ..models.user.orders import Order
from ..models.user.price_limits import UserPricePostDTO
from ..utils.generators import generate_full_link
from ..utils.validators import validate_api_key


class FiveSimAsync(FiveSimBaseClient, AiohttpRequestClient):
    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None
    ) -> None:
        self.__base_url = base_url or Connection.base_url
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
            action: Action | Literal["create", "update", "delete"],
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
        try:
            await self.request(
                method,
                url,
                json=data.model_dump(exclude_none=True),
                no_return=True
            )
            return True
        except ... as exception:
            return False

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
    ) -> Union[CountryWithProducts, list[OperatorWithPrice], ProductWithCountries, list[CountryWithProducts]]:
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

    @validate_api_key
    async def buy_number(
            self,
            product: str,
            country: Optional[str] = BaseValue.ANY,
            operator: Optional[str] = BaseValue.ANY,
            forwarding_number: Optional[str] = None,
            reuse: Optional[bool] = None,
            voice: Optional[bool] = None,
            ref: Optional[str] = None,
            max_price: Optional[float] = None,
    ) -> Order:
        if max_price and operator != BaseValue.ANY:
            raise ValueError("You can't use max_price with operator")

        url = generate_full_link(
            self.__base_url,
            f"user/buy/activation/{country}/{operator}/{product}",
            forwarding="true" if forwarding_number else "false",
            number=forwarding_number,
            reuse=reuse,
            voice=voice,
            ref=ref,
            maxPrice=max_price
        )
        response = await self.request(Method.GET, url)
        return Order(**response)

    @validate_api_key
    async def rent_number(
            self,
            product: str,
            country: Optional[str] = BaseValue.ANY,
            operator: Optional[str] = BaseValue.ANY,
    ) -> Order:
        # Not available at 5sim site
        raise NotImplementedError(f"This method is not available at {self.__base_url.split('/')[2]} site now")

    @validate_api_key
    async def reuse_number(
            self,
            product: str,
            number: str,
    ) -> bool:
        url = generate_full_link(
            self.__base_url,
            f"user/reuse/{product}/{number}",
        )
        try:
            await self.request(Method.GET, url)
            return True
        except ... as exception:
            return False

    @validate_api_key
    async def get_order_info(
            self,
            order_id: Union[str, int]
    ) -> Order:
        url = generate_full_link(
            self.__base_url,
            f"user/check/{order_id}",
        )
        response = await self.request(Method.GET, url)
        return Order(**response)

    @validate_api_key
    async def action_with_order(
            self,
            action: OrderAction | Literal["finish", "cancel", "ban"],
            order_id: Union[str, int]
    ) -> Order:
        url = generate_full_link(
            self.__base_url,
            f"user/{action}/{order_id}",
        )
        response = await self.request(Method.GET, url)
        return Order(**response)

    @validate_api_key
    async def get_rental_info(
            self,
            order_id: int,
    ) -> ...:
        # Not available at 5sim site
        raise NotImplementedError(f"This method is not available at {self.__base_url.split('/')[2]} site now")

    async def get_notification(
            self,
            lang: Literal["ru", "en"] | Lang
    ) -> str | None:
        # IDK what is this method for
        # This method doesn't require api_key...
        url = generate_full_link(
            self.__base_url,
            f"guest/flash/{lang}"
        )
        response = await self.request(Method.GET, url)
        return response.get("text", None)

