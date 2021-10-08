import os
import argparse
from flask import Flask
from src.api import API
from src.db_communicators.mysql_communicator import MySqlUserCommunicator, MySqlFindingCommunicator
from src.db_communicators import ImageCommunicator
from src.db_communicators.mysql_communicator.mysql_executer.mysql_cloud_executor import MyCloudSQLExecuter


def setup_app_credentials_enc():
    credential_path = "google_cloud/junkiapp-619f247751a4.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def create_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mysql-host", default="1.1.1.1")
    parser.add_argument("--mysql-user", default="junkia_user")
    parser.add_argument("--mysql-password", default="junkia_user")
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
    return app


def main():
    parser = create_argparse()
    args = parser.parse_args()
    mysql_executor = MyCloudSQLExecuter(args.mysql_host, args.mysql_user, args.mysql_password)

    credential_path = "google_cloud/junkiapp-619f247751a4.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    
    user_communicator = MySqlUserCommunicator(mysql_executor)
    finding_communicator = MySqlFindingCommunicator(mysql_executor)
    image_communicator = ImageCommunicator()

    api = API(user_communicator, finding_communicator, image_communicator)

    app = create_app(api)
    app.run()


if __name__ == '__main__':
    main()
