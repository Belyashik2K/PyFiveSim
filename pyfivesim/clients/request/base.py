from abc import (
    ABC,
    abstractmethod,
)


class BaseRequestClient(ABC):

    @abstractmethod
    def get_session(self) -> ...:
        ...

    @abstractmethod
    def request(
            self,
            method: str,
            url: str,
            no_return: bool = False,
            **kwargs
    ) -> dict | None:
        ...
