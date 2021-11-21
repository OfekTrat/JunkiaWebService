import os
from time import sleep
from typing import Tuple
from utils.mysql.mysql_executor import IExecutor
from utils.mysql.mysql_executor import MySQLExecutor
from services.finding_service import FindingService
from initializers.finding_initializer import FindingAppInitializer
from communicators.finding_communicators import MySqlFindingCommunicator


def get_running_server() -> Tuple[str, int]:
    return "0.0.0.0", 3000


def test_conn(executor: IExecutor):
    print("Waiting for mysql server to fully upload")
    while True:
        try:
            with executor as (conn, cur):
                print("successful connection")
                break
        except Exception as e:
            sleep(1)


def main():
    server, user, password, debug = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], \
                                    os.environ["MYSQL_PASSWORD"], os.environ["DEBUG_MODE"]
    executor = MySQLExecutor(server, user, password)
    finding_communicator = MySqlFindingCommunicator(executor)
    finding_service = FindingService(finding_communicator)
    host = "0.0.0.0"
    port = os.environ["PORT"]
    app = FindingAppInitializer.get_app(finding_service)
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
