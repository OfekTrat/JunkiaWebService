from flask import request
from .iservice import IService
from models.location import Location
from models.finding import Finding
from .exceptions.finding_exceptions import FindingNotFoundError
from views.message_handler import MessageHandler
from communicators.finding_communicators.ifinding_communicator import IFindingCommunicator


class FindingService(IService):
    def __init__(self, finding_communicator: IFindingCommunicator):
        self.__finding_comm = finding_communicator

    def get_finding(self, finding_id: str):
        if request.method == "GET":
            try:
                finding = self.__finding_comm.get(finding_id)
                return MessageHandler.get_data_msg(finding.to_dict())
            except FindingNotFoundError as e:
                return MessageHandler.get_error_msg(str(e)), 404
        elif request.method == "DELETE":
            return MessageHandler.get_error_msg("Something went wrong"), 400

    def delete_finding(self, finding_id: str):
        if request.method == "DELETE":
            self.__finding_comm.delete(finding_id)
            return MessageHandler.get_success_msg(f"Successful deletion of {finding_id}")
        else:
            return MessageHandler.get_error_msg("Something went wrong"), 400

    def get_finding_by_radius(self):
        try:
            json_data = request.json
            radius = json_data["radius"]
            json_data.pop("radius")
            location = Location.create_from_json(json_data)
            findings = self.__finding_comm.get_by_radius(radius, location)
            findings_as_json = [f.to_dict() for f in findings]
            return MessageHandler.get_data_msg(findings_as_json)
        except KeyError as e:
            return MessageHandler.get_error_msg("Missing important fields"), 400

    def upload_finding(self):
        json_data = request.json
        finding = Finding.create_from_json(json_data)
        self.__finding_comm.upload(finding)
        return MessageHandler.get_success_msg(f"Successful uploading {finding.id}")
