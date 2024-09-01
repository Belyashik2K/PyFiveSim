from typing import (
    Optional,
    Union,
    overload,
    Literal,
    Self,
)
from pydantic import PositiveInt

from .base import FiveSimBaseClient
from .request.aiohttp import AiohttpRequestClient
from ..enums.actions import (
    Action,
    OrderAction,
)

from ..enums.request.connection import Connection
from ..enums.request.method import Method
from ..enums import (
    Category,
    BaseValue,
)
from ..enums.vendor_withdraw import (
    VendorWithdrawMethod,
    VendorWithdrawFee,
)
from ..exceptions import FiveSimDetailedException
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
from ..models.vendor.orders import VendorOrders
from ..models.vendor.payments import VendorPayments
from ..models.vendor.payoff import VendorWithdraw
from ..models.vendor.profile import VendorProfile
from ..models.vendor.wallet import VendorWallets
from ..utils.generators import generate_full_link
from ..utils.validators import validate_api_key


class PyFiveSimAsync(FiveSimBaseClient, AiohttpRequestClient):
    def __init__(
            self,
            api_key: Optional[str] = None,
            base_url: Optional[str] = None
    ) -> None:
        """
        Async client for interact with 5sim API.

        :param api_key: Your API key.
        :param base_url: Base URL for 5sim API.
        """
        self.__base_url = base_url or Connection.base_url
        self._api_key = api_key or None
        self._headers = RequestHeaders(
            Authorization=f"Bearer {api_key}"
        )
        super().__init__(
            headers=self._headers.model_dump(by_alias=True)
        )

    async def __aenter__(self, *args, **kwargs) -> Self:
        return self

    async def __aexit__(self, *args, **kwargs):
        ...

    @validate_api_key
    async def get_user_profile(self) -> UserProfile:
        url = generate_full_link(self.__base_url, "user/profile")
        response = await self.request(Method.GET, url)
        return UserProfile(**response)

    @validate_api_key
    async def get_user_orders(
            self,
            category: Union[Literal["activation", "hosting"], Category],
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserOrders:
        url = generate_full_link(
            self.__base_url,
            "user/orders",
            category=category,
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
            action: Union[Action, Literal["create", "update", "delete"]],
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
        except FiveSimDetailedException:
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
    ) -> Union[
        CountryWithProducts, list[OperatorWithPrice],
        ProductWithCountries, list[CountryWithProducts]
    ]:
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
            return [OperatorWithPrice(name=name, operator_info=Price(**data)) for name, data in
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
        if max_price and country == BaseValue.ANY:
            raise ValueError("You can't use max_price without country")

        url = generate_full_link(
            self.__base_url,
            f"user/buy/activation/{country}/{operator}/{product}",
            forwarding="true" if forwarding_number else "false",
            number=forwarding_number,
            reuse=int(reuse) if reuse else None,
            voice=int(voice) if voice else None,
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
        except FiveSimDetailedException:
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
            action: Union[OrderAction, Literal["finish", "cancel", "ban"]],
            order_id: Union[str, int]
    ) -> Order:
        if action == OrderAction.FINISH:
            current_order = await self.get_order_info(order_id)
            if not current_order.sms:
                action = OrderAction.CANCEL

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

    @validate_api_key
    async def get_vendor_profile(self) -> VendorProfile:
        url = generate_full_link(self.__base_url, "user/vendor")
        response = await self.request(Method.GET, url)
        return VendorProfile(**response)

    @validate_api_key
    async def get_vendor_wallets(self) -> VendorWallets:
        url = generate_full_link(self.__base_url, "vendor/wallets")
        response = await self.request(Method.GET, url)
        return VendorWallets(**response)

    @validate_api_key
    async def get_vendor_orders(
            self,
            category: Union[Literal["activation", "hosting"], Category],
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> VendorOrders:
        url = generate_full_link(
            self.__base_url,
            "vendor/orders",
            category=category,
            limit=limit,
            offset=offset,
            order=order,
            reverse="true" if reverse else "false"
        )
        response = await self.request(Method.GET, url)
        return VendorOrders(**response)

    @validate_api_key
    async def get_vendor_payments(
            self,
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> VendorPayments:
        url = generate_full_link(
            self.__base_url,
            "vendor/payments",
            limit=limit,
            offset=offset,
            order=order,
            reverse="true" if reverse else "false"
        )
        response = await self.request(Method.GET, url)
        return VendorPayments(**response)

    @validate_api_key
    async def create_vendor_withdraw(
            self,
            receiver: str,
            method: Union[Literal["visa", "qiwi", "yandex"], VendorWithdrawMethod],
            amount: float,
            fee: Union[Literal["fkwallet", "payeer", "unitpay"], VendorWithdrawFee],
    ) -> bool:
        url = generate_full_link(self.__base_url, "vendor/withdraw")
        data = VendorWithdraw(
            receiver=receiver,
            method=method,
            amount=amount,
            fee=fee
        )
        try:
            await self.request(
                Method.POST,
                url,
                json=data.model_dump(),
                no_return=True
            )
            return True
        except FiveSimDetailedException:
            return False
