from abc import abstractmethod
from typing import Protocol
from typing import Tuple
from pymysql.connections import Connection
from pymysql.cursors import Cursor


class IExecuter(Protocol):
    @abstractmethod
    def __enter__(self) -> Tuple[Connection, Cursor]:
        raise NotImplementedError()

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @abstractmethod
    def _get_connection(self) -> Connection:
        raise NotImplementedError()
