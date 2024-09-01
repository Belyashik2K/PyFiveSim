from typing import (
    Union,
    Type,
)

from aiohttp import ClientResponse
from httpx import Response

from ..exceptions import *


class RequestExceptionChecker:
    def __init__(self, response: Union[ClientResponse, Response]) -> None:
        self.response = response

    async def run(self):
        response: ClientResponse = self.response
        if response.status == 200 and response.content_type == "application/json":
            return
        exc_text = await response.text() if response.status not in [401, 403] else "Invalid API key"
        exc = self.__get_exception(exc_text.lower(), response.status)
        raise exc(response.status, exc_text)

    def run_sync(self):
        response: Response = self.response
        if response.status_code == 200 and response.headers.get("Content-Type") == "application/json":
            return
        exc_text = response.text if response.status_code not in [401, 403] else "Invalid API key"
        exc = self.__get_exception(exc_text.lower(), response.status_code)
        raise exc(response.status_code, exc_text)

    @staticmethod
    def __get_exception(
            exc_text: str,
            status_code: int
    ) -> Type[FiveSimDetailedException]:
        if status_code in [401, 403]:
            return FiveSimInvalidAPIKey
        if "order not found" in exc_text:
            return FiveSimOrderNotFound
        if "no free phones" in exc_text:
            return FiveSimNoFreePhones
        if "not enough user balance" in exc_text:
            return FiveSimNotEnoughBalance
        if "not enough rating" in exc_text:
            return FiveSimNoEnoughRating
        if "country is incorrect" in exc_text:
            return FiveSimInvalidCountry
        if "bad country" in exc_text:
            return FiveSimInvalidCountry
        if "product is incorrect" in exc_text:
            return FiveSimInvalidProduct
        if "no product" in exc_text:
            return FiveSimInvalidProduct
        if "bad operator" in exc_text:
            return FiveSimInvalidOperator
        if "reuse not possible" in exc_text:
            return FiveSimReuseNotPossible
        if "internal error" in exc_text:
            return FiveSimInternalError
        return FiveSimUnknownError
