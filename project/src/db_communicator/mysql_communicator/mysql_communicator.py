import json
from typing import List, Union, Tuple
import mysql.connector as connector
from mysql.connector import CMySQLConnection, MySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor
from src.db_communicator.idbcommunicator import IDBCommunicator
from src.finding import Finding
from src.location import Location
from src.user import User
from .mysql_query_enum import MySQLQueries
from src.db_communicator.communicator_exceptions import FindingNotFoundError


class MySQLCommunicator(IDBCommunicator):
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "OfekT2021"

    @classmethod
    def upload_finding(cls, finding: Finding):
        query = MySQLQueries.UPLOAD_FINDING.value.format(
           finding_id=finding.id, longitude=finding.location.longitude,
           latitude=finding.location.latitude, image_hash=finding.image_hash,
           tags=json.dumps(finding.tags).replace('"', "").replace("[", "").replace("]", "").replace(" ", "")
        )
        conn, cursor = cls.__execute(query)
        conn.commit()
        cls.__close_session(conn, cursor)


    @classmethod
    def get_finding(cls, finding_id: str) -> Finding:
        query = MySQLQueries.GET_FINDING.value.format(finding_id=finding_id)
        conn, cursor = cls.__execute(query)
        results = cursor.fetchone()
        cls.__close_session(conn, cursor)

        if results is not None:
            return Finding.create_from_json(results)
        else:
            raise FindingNotFoundError(f"finding id {finding_id} not found")

    @classmethod
    def delete_finding(cls, finding_id: str):
        query = MySQLQueries.DELETE_FINDING.value.format(finding_id=finding_id)
        conn, cursor = cls.__execute(query)
        conn.commit()
        cls.__close_session(conn, cursor)

    @classmethod
    def get_finding_by_radius(cls, location: Location, radius: int) -> List[Finding]:
        query = MySQLQueries.RADIUS_SEARCH.value.format(longitude=location.longitude,
                                                        latitude=location.latitude,
                                                        radius=radius)
        conn, cursor = cls.__execute(query)
        finding_results = [Finding.create_from_json(row) for row in cursor.fetchall()]
        cls.__close_session(conn, cursor)
        return finding_results

    @classmethod
    def add_user(cls, user: User):
        pass

    @classmethod
    def __execute(cls, sql_query: str) -> Tuple[Union[CMySQLConnection, MySQLConnection], CMySQLCursor]:
        conn = cls.__get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql_query)
        return conn, cursor

    @classmethod
    def __get_connection(cls) -> Union[CMySQLConnection, MySQLConnection]:
        conn = connector.connect(host=cls.MYSQL_HOST, user=cls.MYSQL_USER, password=cls.MYSQL_PASSWORD)
        return conn

    @classmethod
    def __close_session(cls, conn: Union[CMySQLConnection, MySQLConnection], cursor: CMySQLCursor):
        cursor.close()
        conn.close()
