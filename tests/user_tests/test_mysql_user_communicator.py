import os
import unittest
import random
from models.location import Location
from models.user import User
from utils.mysql.mysql_executor import MySQLExecutor
from communicators.user_communicators import MySqlUserCommunicator
from services.exceptions.user_exceptions import UserNotFoundError, UserAlreadyExistsError


class TestUserCommunicator(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUserCommunicator, self).__init__(*args, **kwargs)
        host, user, password = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]
        self.__executor = MySQLExecutor(host, user, password)
        self.__user_comm = MySqlUserCommunicator(self.__executor)

    def test_get(self):
        user_id = "test"
        user = self.__user_comm.get(user_id)

        assert user.id == user_id
        assert user.tags == ["a", "b", "v"]
        assert user.location.longitude == 1.2
        assert user.location.latitude == -2
        assert user.radius == 10
        assert user.last_notified == "12345678"

    def test_upload(self):
        get_query = "SELECT * FROM junkia.users WHERE id = 'test_upload'"
        delete_query = "DELETE FROM junkia.users WHERE id = 'test_upload'"
        user = User(id="test_upload", tags=list("123"), location=Location(-10.22, 56.33),
                    radius=12, last_notified="12345678")

        self.__user_comm.upload(user)

        with self.__executor as (conn, cursor):
            cursor.execute(get_query)
            result = cursor.fetchall()[0]
            cursor.execute(delete_query)
            conn.commit()

            assert result["id"] == user.id
            assert result["tags"].split(",") == list("123")
            assert result["longitude"] == user.location.longitude
            assert result["latitude"] == user.location.latitude
            assert result["radius"] == user.radius
            assert result["last_notified"] == user.last_notified

    def test_delete(self):
        get_user = "SELECT * FROM junkia.users WHERE id = 'test_delete'"
        upload_user = "INSERT INTO junkia.users (id, tags, longitude, latitude, radius, last_notified) " \
                      "VALUES ('test_delete', '1,2,3', 1, 1, 1, '1234y')"

        with self.__executor as (conn, cursor):
            cursor.execute(upload_user)
            conn.commit()

        self.__user_comm.delete('test_delete')

        with self.__executor as (conn, cursor):
            cursor.execute(get_user)
            result = cursor.fetchall()

        assert type(result) == tuple
        assert len(result) == 0

    def test_update(self):
        get_result = "SELECT * FROM junkia.users WHERE id = 'test_updating'"
        random_lst = list(str(random.randint(100, 999)))
        user = User(id="test_updating", tags=random_lst,
                    location=Location(random.randint(-1800, 1800)/10, random.randint(-900, 900)/10),
                    radius=random.randint(10, 20), last_notified=str(random.randint(1000, 9999)))

        self.__user_comm.update(user)

        with self.__executor as (conn, cursor):
            cursor.execute(get_result)
            result = cursor.fetchall()[0]

            result["tags"] = result['tags'].split(",")
            updated_user = User.create_from_json(result)

            assert updated_user.id == user.id
            assert updated_user.location.longitude == user.location.longitude
            assert updated_user.location.latitude == user.location.latitude
            assert updated_user.radius == user.radius
            assert updated_user.last_notified != user.last_notified
            assert updated_user.tags == user.tags

    def test_get_nonexistant_user(self):
        with self.assertRaises(UserNotFoundError):
            self.__user_comm.get("456uhnkl")

    def test_upload_existing_user(self):
        user = User("test", tags=list("123"), location=Location(-10.22, 56.33),
                    radius=12, last_notified="12345678")

        with self.assertRaises(UserAlreadyExistsError):
            self.__user_comm.upload(user)


if __name__ == '__main__':
    unittest.main()
