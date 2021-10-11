import os
import argparse
from typing import Tuple
from flask import Flask
from src.api import API
from src.db_communicators.mysql_communicator import MySqlUserCommunicator, MySqlFindingCommunicator
from src.db_communicators import ImageCommunicator, MySQLExecutor
from src.db_communicators.mysql_communicator.mysql_executor.iexecutor import IExecutor
from src.db_communicators.mysql_communicator.mysql_executor.mysql_cloud_executor import MyCloudSQLExecutor


def setup_app_credentials_env():
    credential_path = "google_cloud/junkiapp-619f247751a4.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def get_running_server(is_test: bool) -> Tuple[str, int]:
    if is_test:
        return "localhost", 1234
    else:
        return "0.0.0.0", 8080


def create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql-host", default="localhost")
    parser.add_argument("--mysql-user")
    parser.add_argument("--mysql-password")
    parser.add_argument("--test", action="store_true", default=False)
    return parser


def create_app(api: API) -> Flask:
    app = Flask(__name__)
    app.add_url_rule("/finding/<finding_id>", methods=["GET"], view_func=api.get_finding)
    app.add_url_rule("/finding/<finding_id>", methods=["DELETE"], view_func=api.delete_finding)
    app.add_url_rule("/finding/by_radius", methods=["POST"], view_func=api.get_finding_by_radius)
    app.add_url_rule("/finding", methods=["POST"], view_func=api.upload_finding)
    app.add_url_rule("/user", methods=["POST"], view_func=api.add_user)
    app.add_url_rule("/user/<user_id>", methods=["GET"], view_func=api.get_user)
    app.add_url_rule("/user/<user_id>", methods=["PUT"], view_func=api.update_user)
    app.add_url_rule("/image/<image_hash>", methods=["GET"], view_func=api.get_image)
    return app


def get_mysql_communicator(args) -> IExecutor:
    if args.test:
        return MySQLExecutor(args.mysql_host, args.mysql_user, args.mysql_password)
    else:
        return MyCloudSQLExecutor("Irrelevant", args.mysql_user, args.mysql_password)


def main():
    parser = create_argparse()
    setup_app_credentials_env()

    args = parser.parse_args()
    mysql_executor = get_mysql_communicator(args)
    
    user_communicator = MySqlUserCommunicator(mysql_executor)
    finding_communicator = MySqlFindingCommunicator(mysql_executor)
    image_communicator = ImageCommunicator()

    api = API(user_communicator, finding_communicator, image_communicator)

    host, port = get_running_server(args.test)
    app = create_app(api)
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
