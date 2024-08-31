import ssl
from typing import AsyncGenerator

import certifi

from contextlib import asynccontextmanager
from aiohttp import (
    ClientSession,
    TCPConnector,
)

from .base import BaseRequestClient
from ...utils.exception_checker import RequestExceptionChecker


class AiohttpRequestClient(BaseRequestClient):

    def __init__(self, headers: dict):
        self.__headers: dict = headers

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[ClientSession, None]:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)
        session = ClientSession(
            connector=connector,
            headers=self.__headers
        )
        try:
            yield session
        finally:
            await session.close()

    async def request(
            self,
            method: str,
            url: str,
            no_return: bool = False,
            **kwargs
    ) -> dict | None:
        async with self.get_session() as session:  # type: ClientSession
            async with session.request(method, url, **kwargs) as response:
                checker = RequestExceptionChecker(response)
                await checker.run()

                if no_return:
                    return
                return await response.json()
