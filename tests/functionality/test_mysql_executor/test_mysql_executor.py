import os
import unittest
from utils.mysql.mysql_executor import MySQLExecutor


class TestMyExecuter(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMyExecuter, self).__init__(*args, **kwargs)
        server, user, password = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]
        self.__executor = MySQLExecutor(server, user, password)

    def test_execute_one_result(self):
        query = "SELECT * FROM junkia.users"

        with self.__executor as (conn, cursor):
            cursor.execute(query)
            results = cursor.fetchall()

        assert type(results) == list or type(results) == tuple

    def test_commit_upload(self):
        commit_query = "INSERT INTO junkia.users (id, tags, longitude, latitude, radius, last_notified) " \
                "VALUES ('test_commit', '1,2,3', 1, 1, 3, '6567')"
        get_query = "SELECT * FROM junkia.users WHERE id = 'test_commit'"
        delete_query = "DELETE FROM junkia.users WHERE id = 'test_commit'"

        with self.__executor as (conn, cursor):
            cursor.execute(commit_query)
            conn.commit()

            cursor.execute(get_query)
            results = cursor.fetchall()

            assert type(results) == list
            assert len(results) == 1

            cursor.execute(delete_query)
            conn.commit()
            cursor.execute(get_query)
            results = cursor.fetchall()

            assert type(results) == tuple
            assert len(results) == 0


if __name__ == '__main__':
    unittest.main()
