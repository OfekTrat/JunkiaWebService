import pymysql
from typing import Tuple
from pymysql.cursors import Cursor, DictCursor
from pymysql.connections import Connection


class MySQLExecuter:
    def __init__(self, host: str, user: str, password: str):
        self.__host = host
        self.__user = user
        self.__password = password

    def __enter__(self) -> Tuple[Connection, Cursor]:
        self.__conn = self.__get_connection()
        self.__cursor = self.__conn.cursor(DictCursor)
        return self.__conn, self.__cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__cursor.close()
        self.__conn.close()

    def __get_connection(self) -> Connection:
        return pymysql.connect(host=self.__host, user=self.__user, password=self.__password)

