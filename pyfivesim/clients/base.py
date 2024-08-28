from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Optional,
    Union,
)
from pydantic import PositiveInt

from pyfivesim.enums import Category
from pyfivesim.enums.actions import Action
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
            action: Action,
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
            country: Optional[str] = None,
            product: Optional[str] = None,
    ) -> CountryWithProducts | list[OperatorWithPrice] | ProductWithCountries | list[CountryWithProducts]:
        ...
