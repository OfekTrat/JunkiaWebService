import unittest
from src.db_communicators.mysql_communicator import MySQLExecutor


class TestMyExecuter(unittest.TestCase):
    HOST = "localhost"
    USER = "root"
    PASS = "OfekT2021"
    executer = MySQLExecutor(HOST, USER, PASS)

    def test_execute_one_result(self):
        query = "SELECT * FROM junkia.users"

        with self.executer as (conn, cursor):
            cursor.execute(query)
            results = cursor.fetchall()

        assert type(results) == list

    def test_commit_upload(self):
        commit_query = "INSERT INTO junkia.users (id, tags, longitude, latitude, radius, last_notified) " \
                "VALUES ('test_commit', '1,2,3', 1, 1, 3, '6567')"
        get_query = "SELECT * FROM junkia.users WHERE id = 'test_commit'"
        delete_query = "DELETE FROM junkia.users WHERE id = 'test_commit'"

        with self.executer as (conn, cursor):
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
