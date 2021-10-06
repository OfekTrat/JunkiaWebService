from typing import List
from pymysql.err import IntegrityError
from project.src.user import User
from .queries import Queries
from .exceptions import UserNotFoundError, UserAlreadyExistsError
from project.src.db_communicators.mysql_communicator.mysql_executer import MySQLExecuter
from project.src.db_communicators.mysql_communicator.mysql_communicator_abs import MySQLCommunicatorAbs


class MySqlUserCommunicator(MySQLCommunicatorAbs):
    HOST = "localhost"
    USER = "root"
    PASS = "OfekT2021"

    @classmethod
    def get(cls, user_id: str) -> User:
        get_query = Queries.GET.value.format(user_id=user_id)
        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        result = executer.execute(get_query)
        executer.close()

        if len(result) == 0:
            raise UserNotFoundError()

        user_as_dict = result[0]
        user_as_dict["tags"] = cls._str_to_tags(user_as_dict["tags"])
        return User.create_from_json(user_as_dict)

    @classmethod
    def upload(cls, user: User):
        upload_query = Queries.UPLOAD.value.format(
            user_id=user.id,
            tags=cls._tags_to_str(user.tags),
            longitude=user.location.longitude,
            latitude=user.location.latitude,
            radius=user.radius,
            last_notified=user.last_notified
        )
        try:
            executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
            executer.commit(upload_query)
            executer.close()
        except IntegrityError:
            raise UserAlreadyExistsError()

    @classmethod
    def delete(cls, user_id: str):
        delete_query = Queries.DELETE.value.format(user_id=user_id)
        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        executer.commit(delete_query)
        executer.close()

    @classmethod
    def update(cls, user: User):
        update_query = Queries.UPDATE.value.format(
            tags=cls._tags_to_str(user.tags),
            longitude=user.location.longitude,
            latitude=user.location.latitude,
            radius=user.radius,
            user_id=user.id
        )
        executer = MySQLExecuter(cls.HOST, cls.USER, cls.PASS)
        executer.commit(update_query)
        executer.close()

