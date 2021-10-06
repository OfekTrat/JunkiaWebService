from flask import Flask, request
from project.src.user import User
from project.src.finding import Finding
from project.src.location import Location
from project.src.message_handler import MessageHandler
from project.src.db_communicators.mysql_communicator import MySqlUserCommunicator, MySqlFindingCommunicator, \
    FindingNotFoundError, UserAlreadyExistsError, UserNotFoundError


app = Flask(__name__)


@app.route("/finding/<finding_id>", methods=["GET", "DELETE"])
def get_or_delete_finding(finding_id: str):
    if request.method == "GET":
        try:
            finding = MySqlFindingCommunicator.get(finding_id)
            return MessageHandler.get_data_msg(finding.to_dict())
        except FindingNotFoundError as e:
            return MessageHandler.get_error_msg(str(e)), 404
    elif request.method == "DELETE":
        MySqlFindingCommunicator.delete(finding_id)
        return MessageHandler.get_success_msg(f"Successful deletion of {finding_id}")


@app.route("/finding/by_radius", methods=["POST"])
def get_finding_by_radius():
    try:
        json_data = request.json
        radius = json_data["radius"]
        json_data.pop("radius")
        location = Location.create_from_json(json_data)
        findings = MySqlFindingCommunicator.get_by_radius(radius, location)
        findings_as_json = [f.to_dict() for f in findings]
        return MessageHandler.get_data_msg(findings_as_json)
    except KeyError as e:
        return MessageHandler.get_error_msg("Missing important fields"), 400


@app.route("/finding", methods=["POST"])
def upload_finding():
    json_data = request.json
    finding = Finding.create_from_json(json_data)
    MySqlFindingCommunicator.upload(finding)
    return MessageHandler.get_success_msg(f"Successful uploading {finding.id}")


@app.route("/user", methods=["POST"])
def add_user():
    try:
        user_as_json = request.json
        user = User.create_from_json(user_as_json)
        MySqlUserCommunicator.upload(user)
        return MessageHandler.get_success_msg(f"Successful adding user {user.id}")
    except UserAlreadyExistsError as e:
        return MessageHandler.get_error_msg(str(e)), 400
    except KeyError as e:
        return MessageHandler.get_error_msg("Probably Bad Request"), 400
    except AttributeError:
        return MessageHandler.get_error_msg("Probably not a json"), 400


@app.route("/user/<user_id>", methods=["GET", "PUT"])
def update_or_get_user(user_id: str):
    try:
        if request.method == "GET":
            user = MySqlUserCommunicator.get(user_id)
            return MessageHandler.get_data_msg(user.to_dict())
        elif request.method == "PUT":
            json_data = request.json
            user = User.create_from_json(json_data)
            MySqlUserCommunicator.update(user)
            return MessageHandler.get_success_msg("Successful Updating")
    except UserNotFoundError as e:
        return MessageHandler.get_error_msg(str(e)), 404


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()


#TODO Add user to uploading finding, and to the DB
#     and handling when a user does not exist.
# Split communicators to three communicators: UserCommunicator, FindingCommunicator,
#   ImageCommunicator (get, upload, update). Intialize the interface first.
#TODO Handle Errors in endpoinst (int the routes)
#TODO Add Finding Grabage Collector
#TODO Add CLI arguments to app
#TODO Add delete by time (for Grabage Collector) endpoint
#TODO Add messages to exceptions
