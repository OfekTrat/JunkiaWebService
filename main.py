import os
from time import sleep
from typing import Tuple

from app_initializer import AppInitializer

from services.user_service import UserService
from services.image_service import ImageService
from services.finding_service import FindingService

from utils.mysql.mysql_executor import IExecutor
from utils.mysql.mysql_executor import MySQLExecutor

from communicators.user_communicators import MySqlUserCommunicator
from communicators.image_communicators import SimpleImageCommunicator
from communicators.finding_communicators import MySqlFindingCommunicator
from communicators.interfaces import IUserCommunicator, IFindingCommunicator, IImageCommunicator


def get_running_server() -> Tuple[str, int]:
    return "0.0.0.0", 3000


def get_communicators(executor: IExecutor) -> Tuple[IUserCommunicator, IFindingCommunicator, IImageCommunicator]:
    return MySqlUserCommunicator(executor), MySqlFindingCommunicator(executor), SimpleImageCommunicator()


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
    test_conn(executor)
    user_communicator, finding_communicator, image_communicator = get_communicators(executor)

    host, port = get_running_server()

    finding_service = FindingService(finding_communicator)
    user_service = UserService(user_communicator)
    image_service = ImageService(image_communicator)

    app_initializer = AppInitializer()
    app_initializer.add_finding_service(finding_service)
    app_initializer.add_user_service(user_service)
    app_initializer.add_image_service(image_service)

    app = app_initializer.get_app()
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
