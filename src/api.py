import os
from flask import request
from src.db_communicators.interfaces import IUserCommunicator, IImageCommunicator, IFindingCommunicator
from src.user import User
from src.finding import Finding
from .image import Image
from .location import Location
from src.message_handler import MessageHandler
from src.db_communicators.mysql_communicator import FindingNotFoundError, UserAlreadyExistsError, UserNotFoundError
from src.db_communicators.image_communicator.exceptions import ImageNotFoundError, ImageAlreadyExistsError


class API:
    def __init__(self, user_communicator: IUserCommunicator,
                 finding_communicator: IFindingCommunicator, image_communicator: IImageCommunicator):
        self.__user_comm = user_communicator
        self.__finding_comm = finding_communicator
        self.__image_comm = image_communicator

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
            return MessageHandler.get_error_msg("Something went wrong")

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

    def add_user(self):
        try:
            user_as_json = request.json
            user = User.create_from_json(user_as_json)
            self.__user_comm.upload(user)
            return MessageHandler.get_success_msg(f"Successful adding user {user.id}")
        except UserAlreadyExistsError as e:
            return MessageHandler.get_error_msg(str(e)), 400
        except KeyError as e:
            return MessageHandler.get_error_msg("Probably Bad Request"), 400
        except AttributeError:
            return MessageHandler.get_error_msg("Probably not a json"), 400

    def get_user(self, user_id: str):
        try:
            if request.method == "GET":
                user = self.__user_comm.get(user_id)
                return MessageHandler.get_data_msg(user.to_dict())
            else:
                MessageHandler.get_error_msg("Something went wrong"), 400
        except UserNotFoundError as e:
            return MessageHandler.get_error_msg(str(e)), 404

    def update_user(self, user_id: str):
        if request.method == "PUT":
            try:
                json_data = request.json
                user = User.create_from_json(json_data)
                self.__user_comm.update(user)
                return MessageHandler.get_success_msg("Successful Updating")
            except UserNotFoundError as e:
                return MessageHandler.get_error_msg(str(e)), 404
            except Exception as e:
                return MessageHandler.get_error_msg(str(e)), 400
        else:
            MessageHandler.get_error_msg("Something went wrong"), 400

    def get_image(self, image_hash: str):
        try:
            image = self.__image_comm.get(image_hash)
            return image.to_json()
        except ImageNotFoundError as e:
            return MessageHandler.get_error_msg("File Not Found"), 404
        except Exception as e:
            return MessageHandler.get_error_msg(str(e))

    def upload_image(self):
        if request.method == "POST":
            try:
                image = Image.from_json(request.json)
                self.__image_comm.upload(image)
                return MessageHandler.get_success_msg("Successful Image Upload")
            except ImageAlreadyExistsError as e:
                return MessageHandler.get_error_msg("Image Already Exists"), 200
        else:
            return MessageHandler.get_error_msg("Something went wrong"), 400



