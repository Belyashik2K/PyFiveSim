import ssl
import certifi

from contextlib import contextmanager
from typing import Generator
from httpx import Client, Response

from pyfivesim.clients.request.base import BaseRequestClient
from pyfivesim.utils.exception_checker import RequestExceptionChecker


class HttpxRequestClient(BaseRequestClient):

    def __init__(self, headers: dict):
        self.__headers: dict = headers

    @contextmanager
    def get_session(self) -> Generator[Client, None, None]:
        verify = ssl.create_default_context(cafile=certifi.where())
        client = Client(headers=self.__headers, verify=verify)
        try:
            yield client
        finally:
            client.close()

    def request(
            self,
            method: str,
            url: str,
            no_return: bool = False,
            **kwargs
    ) -> dict | None:
        with self.get_session() as session: # type: Client
            response = session.request(method, url, **kwargs)
            checker = RequestExceptionChecker(response)
            checker.run_sync()

            if no_return:
                return
            return response.json()
