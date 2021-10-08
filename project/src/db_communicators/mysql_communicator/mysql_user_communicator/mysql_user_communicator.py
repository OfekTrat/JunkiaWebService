from pymysql.err import IntegrityError
from project.src.user import User
from .queries import Queries
from .exceptions import UserNotFoundError, UserAlreadyExistsError
from project.src.db_communicators.mysql_communicator.mysql_executer import MySQLExecuter
from project.src.db_communicators.mysql_communicator.mysql_communicator_abs import MySQLCommunicatorAbs
from project.src.db_communicators.interfaces.iuser_communicator import IUserCommunicator


class MySqlUserCommunicator(MySQLCommunicatorAbs, IUserCommunicator):
    def __init__(self, mysql_executor: MySQLExecuter):
        super().__init__()
        self.__executor = mysql_executor

    def get(self, user_id: str) -> User:
        get_query = Queries.GET.value.format(user_id=user_id)

        with self.__executor as (conn, cursor):
            cursor.execute(get_query)
            result = cursor.fetchall()

        if len(result) == 0:
            raise UserNotFoundError()

        user_as_dict = result[0]
        user_as_dict["tags"] = self._str_to_tags(user_as_dict["tags"])
        return User.create_from_json(user_as_dict)

    def upload(self, user: User):
        upload_query = Queries.UPLOAD.value.format(
            user_id=user.id,
            tags=self._tags_to_str(user.tags),
            longitude=user.location.longitude,
            latitude=user.location.latitude,
            radius=user.radius,
            last_notified=user.last_notified
        )
        with self.__executor as (conn, cursor):
            try:
                cursor.execute(upload_query)
                conn.commit()
            except IntegrityError:
                raise UserAlreadyExistsError()

    def delete(self, user_id: str):
        delete_query = Queries.DELETE.value.format(user_id=user_id)

        with self.__executor as (conn, cursor):
            cursor.execute(delete_query)
            conn.commit()

    def update(self, user: User):
        update_query = Queries.UPDATE.value.format(
            tags=self._tags_to_str(user.tags),
            longitude=user.location.longitude,
            latitude=user.location.latitude,
            radius=user.radius,
            user_id=user.id
        )
        with self.__executor as (conn, cursor):
            cursor.execute(update_query)
            conn.commit()
