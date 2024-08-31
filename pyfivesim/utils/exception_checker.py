from typing import Union

from aiohttp import ClientResponse
from httpx import Response

from ..exceptions import FiveSimDetailedException


class RequestExceptionChecker:
    def __init__(self, response: Union[ClientResponse, Response]) -> None:
        self.response = response

        self.__mapped_exceptions = {
            400: "Bad request",
            401: "API key is invalid",
            403: "Forbidden",
            404: "Not found",
            405: "Method not allowed",
            406: "Not acceptable",
            408: "Request timeout",
            409: "Conflict",
            410: "Gone",
            429: "Too many requests",
            500: "Internal server error",
            502: "Bad gateway",
            503: "Service unavailable",
            504: "Gateway timeout",
        }

    async def run(self):
        response: ClientResponse = self.response
        if self.response.status == 200 and self.response.content_type == "application/json":
            return
        exception_text = await response.text() or self.__mapped_exceptions.get(response.status)
        raise FiveSimDetailedException(
            status_code=self.response.status if "free" not in exception_text else 400,
            data=exception_text
        )

    def run_sync(self):
        response: Response = self.response
        if self.response.status_code == 200 and self.response.headers.get("Content-Type") == "application/json":
            return
        exception_text = self.response.text or self.__mapped_exceptions.get(response.status_code)
        raise FiveSimDetailedException(
            status_code=self.response.status_code if "free" not in exception_text else 400,
            data=exception_text
        )
