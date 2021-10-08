from flask import Flask
from project.api import API
from project.src.db_communicators.mysql_communicator import MySqlUserCommunicator, MySqlFindingCommunicator
from project.src.db_communicators.image_communicator import ImageCommunicator
from project.src.db_communicators.mysql_communicator.mysql_executer import MySQLExecuter


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
    mysql_executor = MySQLExecuter("localhost", "root", "OfekT2021")
    user_communicator = MySqlUserCommunicator(mysql_executor)
    finding_communicator = MySqlFindingCommunicator(mysql_executor)
    image_communicator = ImageCommunicator

    api = API(user_communicator, finding_communicator, image_communicator)

    app = create_app(api)
    app.run()


if __name__ == '__main__':
    main()