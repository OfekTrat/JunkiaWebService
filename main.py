import os
from typing import Tuple
from flask import Flask
from src.api import API
from src.db_communicators.interfaces import IUserCommunicator, IFindingCommunicator, IImageCommunicator
from src.db_communicators.mysql_communicator import MySqlUserCommunicator, MySqlFindingCommunicator
from src.db_communicators import ImageCommunicator, MySQLExecutor
from src.db_communicators.mysql_communicator.mysql_executor.iexecutor import IExecutor
from time import sleep


def get_running_server() -> Tuple[str, int]:
    return "0.0.0.0", 3000


def create_app(api: API) -> Flask:
    app = Flask(__name__)
    app.add_url_rule("/finding/<finding_id>", methods=["GET"], view_func=api.get_finding)
    app.add_url_rule("/finding/<finding_id>", methods=["DELETE"], view_func=api.delete_finding)
    app.add_url_rule("/finding/by_radius", methods=["POST"], view_func=api.get_finding_by_radius)
    app.add_url_rule("/finding", methods=["POST"], view_func=api.upload_finding)
    app.add_url_rule("/user", methods=["POST"], view_func=api.add_user)
    app.add_url_rule("/user/<user_id>", methods=["GET"], view_func=api.get_user)
    app.add_url_rule("/user/<user_id>", methods=["PUT"], view_func=api.update_user)
    app.add_url_rule("/user/<user_id>", methods=["DELETE"], view_func=api.delete_user)
    app.add_url_rule("/image/<image_hash>", methods=["GET"], view_func=api.get_image)
    app.add_url_rule("/image", methods=["POST"], view_func=api.upload_image)
    app.add_url_rule("/image", methods=["DELETE"], view_func=api.delete_image)
    return app


def get_communicators(executor: IExecutor) -> Tuple[IUserCommunicator, IFindingCommunicator, IImageCommunicator]:
    return MySqlUserCommunicator(executor), MySqlFindingCommunicator(executor), ImageCommunicator()


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
    server, user, password = os.environ["MYSQL_SERVER"], os.environ["MYSQL_USER"], os.environ["MYSQL_PASSWORD"]
    executor = MySQLExecutor(server, user, password)
    test_conn(executor)
    user_communicator, finding_communicator, image_communicator = get_communicators(executor)
    api = API(user_communicator, finding_communicator, image_communicator)
    host, port = get_running_server()
    app = create_app(api)
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
