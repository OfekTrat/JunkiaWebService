import unittest
from project.src.db_communicators.mysql_communicator.mysql_executer.mysql_executer import MySQLExecuter


class TestMyExecuter(unittest.TestCase):
    HOST = "localhost"
    USER = "root"
    PASS = "OfekT2021"

    def test_execute_one_result(self):
        query = "SELECT * FROM junkia.users"

        executer = MySQLExecuter(self.HOST, self.USER, self.PASS)
        results = executer.execute(query)
        executer.close()

        assert type(results) == list

    def test_execute_multiple_results(self):
        query = "SELECT * FROM junkia.users"

        executer = MySQLExecuter(self.HOST, self.USER, self.PASS)
        results = executer.execute(query)
        executer.close()

        assert type(results) == list

    def test_commit_upload(self):
        commit_query = "INSERT INTO junkia.users (id, tags, longitude, latitude, radius, last_notified) " \
                "VALUES ('test_commit', '1,2,3', 1, 1, 3, '6567')"
        get_query = "SELECT * FROM junkia.users WHERE id = 'test_commit'"
        delete_query = "DELETE FROM junkia.users WHERE id = 'test_commit'"

        executer = MySQLExecuter(self.HOST, self.USER, self.PASS)
        executer.commit(commit_query)
        results = executer.execute(get_query)

        assert type(results) == list
        assert len(results) == 1

        executer.commit(delete_query)
        results = executer.execute(get_query)

        assert type(results) == list
        assert len(results) == 0

        executer.close()


if __name__ == '__main__':
    unittest.main()
