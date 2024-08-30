from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Optional,
    Union,
    Literal,
)
from pydantic import PositiveInt

from pyfivesim.enums import (
    Category,
    Action,
    BaseValue,
)
from pyfivesim.enums.actions import OrderAction
from pyfivesim.enums.langs import Lang
from pyfivesim.models.guest.countries import Country
from pyfivesim.models.guest.prices import (
    CountryWithProducts,
    OperatorWithPrice,
    ProductWithCountries,
)
from pyfivesim.models.user import (
    UserOrders,
    UserProfile,
    UserPayments,
    UserPriceLimit,
)
from pyfivesim.models.user.orders import Order


class FiveSimBaseClient(ABC):

    @abstractmethod
    def get_user_profile(self) -> UserProfile:
        ...

    @abstractmethod
    def get_user_orders(
            self,
            category: Union[str, Category],
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserOrders:
        ...

    @abstractmethod
    def get_user_payments(
            self,
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserPayments:
        ...

    @abstractmethod
    def get_user_price_limits(self) -> list[UserPriceLimit]:
        ...

    @abstractmethod
    def action_with_user_price_limits(
            self,
            action: Action | Literal["create", "update", "delete"],
            product_name: str,
            price: Optional[float] = None
    ) -> bool:
        ...

    @abstractmethod
    def get_countries_list(self) -> list[Country]:
        ...

    @abstractmethod
    def get_prices(
            self,
            *args,
            **kwargs
    ) -> CountryWithProducts | list[OperatorWithPrice] | ProductWithCountries | list[CountryWithProducts]:
        ...

    @abstractmethod
    def buy_number(
            self,
            product: str,
            country: Optional[str] = BaseValue.ANY,
            operator: Optional[str] = BaseValue.ANY,
            forwarding_number: Optional[str] = None,
            reuse: Optional[bool] = False,
            voice: Optional[bool] = False,
            ref: Optional[str] = None,
            max_price: Optional[float] = None,
    ) -> Order:
        ...

    @abstractmethod
    def rent_number(
            self,
            product: str,
            country: Optional[str] = BaseValue.ANY,
            operator: Optional[str] = BaseValue.ANY,
    ) -> Order:
        ...

    @abstractmethod
    def reuse_number(
            self,
            product: str,
            number: str,
    ) -> bool:
        ...

    @abstractmethod
    def get_order_info(
            self,
            order_id: int,
    ) -> Order:
        ...

    @abstractmethod
    def action_with_order(
            self,
            action: OrderAction | Literal["finish", "cancel", "ban"],
            order_id: Union[str, int],
    ) -> Order:
        ...

    @abstractmethod
    def get_rental_info(
            self,
            order_id: int,
    ) -> ...:
        ...

    @abstractmethod
    def get_notification(
            self,
            lang: Literal["ru", "en"] | Lang
    ) -> str | None:
        ...

    # Vendor methods in development
    @abstractmethod
    def get_vendor_profile(self) -> ...:
        ...

    @abstractmethod
    def get_vendor_balances(self) -> ...:
        ...

    @abstractmethod
    def get_vendor_orders(self) -> ...:
        ...

    @abstractmethod
    def get_vendor_payments(self) -> ...:
        ...

    @abstractmethod
    def create_vendor_withdraw(self) -> bool:
        ...