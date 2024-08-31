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

from ..enums import (
    Category,
    BaseValue,
)
from ..enums.actions import Action, OrderAction
from ..enums.vendor_withdraw import (
    VendorWithdrawFee,
    VendorWithdrawMethod,
)
from ..models.guest.countries import Country
from ..models.guest.prices import (
    OperatorWithPrice,
    CountryWithProducts,
    ProductWithCountries,
)
from ..models.guest.products import Product
from ..models.user import (
    UserProfile,
    UserOrders,
    UserPayments,
    UserPriceLimit,
)
from ..models.user.orders import Order
from ..models.vendor.orders import VendorOrders
from ..models.vendor.payments import VendorPayments
from ..models.vendor.profile import VendorProfile
from ..models.vendor.wallet import VendorWallets


class FiveSimBaseClient(ABC):
    """
    Base class for all 5sim clients.
    """

    @abstractmethod
    def get_user_profile(self) -> UserProfile:
        """
        Provides profile data: email, balance and rating.

        Docs: https://5sim.net/docs#balance
        """
        ...

    @abstractmethod
    def get_user_orders(
            self,
            category: Union[Literal["activation", "hosting"], Category],
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserOrders:
        """
        Provides orders history by choosen category.

        Docs: https://5sim.net/docs#order-history

        :param category: Category
        :param limit: Pagination limit
        :param offset: Pagination offset
        :param order: Pagination order, should be field name
        :param reverse: Reverse order or not
        """
        ...

    @abstractmethod
    def get_user_payments(
            self,
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> UserPayments:
        """
        Provides payments history.

        Docs: https://5sim.net/docs#payments-history

        :param limit: Pagination limit
        :param offset: Pagination offset
        :param order: Pagination order, should be field name
        :param reverse: Reverse order or not
        """
        ...

    @abstractmethod
    def get_user_price_limits(self) -> list[UserPriceLimit]:
        """
        Get a list of established price limits for the user.

        Docs: https://5sim.net/docs#get-list-of-price-limits
        """
        ...

    @abstractmethod
    def action_with_user_price_limits(
            self,
            action: Union[Action, Literal["create", "update", "delete"]],
            product_name: str,
            price: Optional[float] = None
    ) -> bool:
        """
        Create, update or delete price limit for the user.

        Docs: https://5sim.net/docs#create-or-update-price-limits,

        https://5sim.net/docs#delete-price-limit

        :param action: Action which should be done
        :param product_name: Product name
        :param price: Price limit
        """
        ...

    @abstractmethod
    def get_countries_list(self) -> list[Country]:
        """
        Returns a list of countries with available operators for purchase.

        Docs: https://5sim.net/docs#get-countries-list
        """
        ...

    @abstractmethod
    def get_available_products(
            self,
            country: str,
            operator: str
    ) -> list[Product]:
        """
        Returns a list of available products for purchase in the selected country and operator.

        Docs: https://5sim.net/docs#products-request

        :param country: Country name
        :param operator: Operator name
        """
        ...

    @abstractmethod
    def get_prices(
            self,
            *args,
            **kwargs
    ) -> Union[
        CountryWithProducts, list[OperatorWithPrice],
        ProductWithCountries, list[CountryWithProducts]
    ]:
        """
        Returns product prices for countries and products.

        Docs: https://5sim.net/docs#prices-request,

        https://5sim.net/docs#prices-by-country,

        https://5sim.net/docs#prices-by-product,

        https://5sim.net/docs#prices-by-country-and-product

        :param country: Country name
        :param product: Product name
        """
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
        """
        Buy activation number.

        Docs: https://5sim.net/docs#purchase-request

        :param product: Product name
        :param country: The country, "any" - any country
        :param operator: The operator, "any" - any operator
        :param forwarding_number: Number for which the call will be forwarded, only the Russian numbers, 11 digits, without the + sign
        :param reuse: Buy with the ability to reuse the number, if available
        :param voice: Buy with the ability to receive a call from the robot, if available
        :param ref: Your referral key if you have it, if you are developer of the software (read more on docs)
        :param max_price: Max price specified in the Purchase method parameters shall have priority over the settings adjusted in the Max purchase price section and shall work only if the operator value is set as "any"
        """
        ...

    @abstractmethod
    def rent_number(
            self,
            product: str,
            country: Optional[str] = BaseValue.ANY,
            operator: Optional[str] = BaseValue.ANY,
    ) -> Order:
        """
        Rent a number.

        Docs: https://5sim.net/docs#buy-hosting-number

        :param product: Product name (3hours, 1day)
        :param country: The country, "any" - any country
        :param operator: The operator, "any" - any operator
        """
        ...

    @abstractmethod
    def reuse_number(
            self,
            product: str,
            number: str,
    ) -> bool:
        """
        Reuse the number.

        Docs: https://5sim.net/docs#rebuy-number

        :param product: Product name
        :param number: Number which should be reused
        """
        ...

    @abstractmethod
    def get_order_info(
            self,
            order_id: int,
    ) -> Order:
        """
        Get order information.

        Docs: https://5sim.net/docs#check-order-get-sms

        :param order_id: Order id
        """
        ...

    @abstractmethod
    def action_with_order(
            self,
            action: Union[OrderAction, Literal["finish", "cancel", "ban"]],
            order_id: Union[str, int],
    ) -> Order:
        """
        Finish, cancel or ban the order.

        Docs: https://5sim.net/docs#finish-order,

        https://5sim.net/docs#cancel-order,

        https://5sim.net/docs#ban-order

        :param action: Action which should be done
        :param order_id: Order id
        """
        ...

    @abstractmethod
    def get_rental_info(
            self,
            order_id: int,
    ) -> ...:
        """
        Get rental info.

        Docs: https://5sim.net/docs#sms-inbox-list

        :param order_id: Order id
        """
        ...

    @abstractmethod
    def get_vendor_profile(self) -> VendorProfile:
        """
        Get vendor profile data.

        Docs: https://5sim.net/docs#vendor-statistic
        """
        ...

    @abstractmethod
    def get_vendor_wallets(self) -> VendorWallets:
        """
        Available reserves currency for partner.

        Docs: https://5sim.net/docs#wallets-reserve
        """
        ...

    @abstractmethod
    def get_vendor_orders(
            self,
            category: Union[Literal["activation", "hosting"], Category],
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> VendorOrders:
        """
        Provides vendor's orders history by chosen category.

        Docs: https://5sim.net/docs#vendor-orders-history

        :param category: Category
        :param limit: Pagination limit
        :param offset: Pagination offset
        :param order: Pagination order, should be field name
        :param reverse: Reverse order or not
        """
        ...

    @abstractmethod
    def get_vendor_payments(
            self,
            limit: Optional[PositiveInt] = None,
            offset: Optional[PositiveInt] = None,
            order: Optional[str] = None,
            reverse: Optional[bool] = None
    ) -> VendorPayments:
        """
        Provides vendor's payments history.

        :param limit: Pagination limit
        :param offset: Pagination offset
        :param order: Pagination order, should be field name
        :param reverse: Reverse order or not
        """
        ...

    @abstractmethod
    def create_vendor_withdraw(
            self,
            receiver: str,
            method: Union[Literal["visa", "qiwi", "yandex"], VendorWithdrawMethod],
            amount: float,
            fee: Union[Literal["fkwallet", "payeer", "unitpay"], VendorWithdrawFee],
    ) -> bool:
        """
        Create payouts for a partner.

        Docs: https://5sim.net/docs#create-payouts

        :param receiver: Receiver
        :param method: 	Output method (visa/qiwi/yandex)
        :param amount: Amount
        :param fee: Payment system (fkwallet/payeer/unitpay)
        """
        ...
