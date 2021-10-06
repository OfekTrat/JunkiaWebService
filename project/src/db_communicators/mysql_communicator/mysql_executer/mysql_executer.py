import pymysql
from typing import Dict, List, Tuple, Union
from pymysql.cursors import Cursor, DictCursor
from pymysql.connections import Connection


class MySQLExecuter:
    def __init__(self, host: str, user: str, password: str):
        self.__conn = self.__get_connection(host, user, password)
        self.__cursor = self.__conn.cursor(DictCursor)

    @staticmethod
    def __get_connection(host: str, user: str, password: str) -> Connection:
        return pymysql.connect(host=host, user=user, password=password)

    def execute(self, query: str) -> List[Dict[str, Union[int, float, str]]]:
        self.__cursor.execute(query)
        results = self.__cursor.fetchall()

        if results == ():
            return list()

        return results

    def commit(self, query: str):
        self.__cursor.execute(query)
        self.__conn.commit()

    def close(self):
        self.__cursor.close()
        self.__conn.close()
