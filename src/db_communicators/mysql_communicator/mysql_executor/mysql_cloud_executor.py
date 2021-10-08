from typing import Tuple
from pymysql.cursors import Cursor, DictCursor
from pymysql.connections import Connection
from google.cloud.sql.connector import connector
from .iexecutor import IExecutor


class MyCloudSQLExecutor(IExecutor):
    def __init__(self, host: str, user: str, password: str):
        self.__host = host
        self.__user = user
        self.__password = password

    def __enter__(self) -> Tuple[Connection, Cursor]:
        self.__conn = self._get_connection()
        self.__cursor = self.__conn.cursor(DictCursor)
        return self.__conn, self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__conn.close()

    def _get_connection(self) -> Connection:
        return connector.connect(
            "junkiapp:us-central1:junkia",
            "pymysql",
            user=self.__user,
            password=self.__password,
            db="junkia"
        )

