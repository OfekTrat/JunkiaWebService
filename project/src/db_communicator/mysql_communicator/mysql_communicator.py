from typing import List, Union, Tuple, Dict, Any
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor
from project.src.finding import Finding
from project.src.location import Location
from project.src.user import User
from project.src.db_communicator.communicator_exceptions import FindingNotFoundError, UserNotFoundError, \
    UserAlreadyExistError
from project.src.db_communicator.idbcommunicator import IDBCommunicator
from project.src.db_communicator.mysql_communicator.mysql_query_builder import MySQLQueryBuilder


class MySQLCommunicator(IDBCommunicator):
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "OfekT2021"

    @classmethod
    def upload_finding(cls, finding: Finding):
        query = MySQLQueryBuilder.build_upload_finding(finding)
        conn, cursor = cls.__execute(query)
        conn.commit()
        cls.__close_session(conn, cursor)


    @classmethod
    def get_finding(cls, finding_id: str) -> Finding:
        query = MySQLQueryBuilder.build_get_finding(finding_id)
        conn, cursor = cls.__execute(query)
        results = cursor.fetchone()
        cls.__close_session(conn, cursor)

        if results is not None:
            formatted_results = cls.__change_tags_in_dict(results)
            return Finding.create_from_json(formatted_results)
        else:
            raise FindingNotFoundError(f"finding id {finding_id} not found")

    @classmethod
    def delete_finding(cls, finding_id: str):
        query = MySQLQueryBuilder.build_delete_finding(finding_id)
        conn, cursor = cls.__execute(query)
        conn.commit()
        cls.__close_session(conn, cursor)

    @classmethod
    def get_finding_by_radius(cls, location: Location, radius: Union[int, float]) -> List[Finding]:
        query = MySQLQueryBuilder.build_radius_finding_search(location, radius)
        print(query)
        conn, cursor = cls.__execute(query)
        finding_results = [Finding.create_from_json(cls.__change_tags_in_dict(row)) for row in cursor.fetchall()]
        cls.__close_session(conn, cursor)
        return finding_results

    @classmethod
    def __change_tags_in_dict(cls, json: Dict[str, Any]) -> Dict[str, Any]:
        json_copy = json.copy()

        json_copy["tags"] = json_copy["tags"].split(",")
        return json_copy

    @classmethod
    def add_user(cls, user: User):
        try:
            query = MySQLQueryBuilder.build_add_user(user)
            conn, cursor = cls.__execute(query)
            conn.commit()
            cls.__close_session(conn, cursor)
        except pymysql.err.IntegrityError as e:
            raise UserAlreadyExistError(f"User {user.id} already exists")

    @classmethod
    def get_user(cls, user_id: str) -> User:
        query = MySQLQueryBuilder.build_get_user(user_id)
        conn, cursor = cls.__execute(query)
        user_as_json = cursor.fetchone()
        cls.__close_session(conn, cursor)

        if user_as_json is None:
            raise UserNotFoundError

        user_as_json = cls.__change_tags_in_dict(user_as_json)
        return User.create_from_json(user_as_json)

    @classmethod
    def update_user(cls, user_to_update: User):
        query = MySQLQueryBuilder.build_update_user(user_to_update)
        conn, cursor = cls.__execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def _delete_user(cls, user_id: str):
        query = f"DELETE FROM junkia.users WHERE id = '{user_id}'"
        conn, cursor = cls.__execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def __execute(cls, sql_query: str) -> Tuple[Connection, Cursor]:
        conn = cls.__get_connection()
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(sql_query)
        return conn, cursor

    @classmethod
    def __get_connection(cls) -> Connection:
        conn = pymysql.connect(host=cls.MYSQL_HOST, user=cls.MYSQL_USER, password=cls.MYSQL_PASSWORD)
        return conn

    @classmethod
    def __close_session(cls, conn: Connection, cursor: Cursor):
        cursor.close()
        conn.close()
