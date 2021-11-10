from flask import request
from models import User
from .exceptions import UserNotFoundError, UserAlreadyExistsError
from views.message_handler import MessageHandler
from communicators.interfaces import IUserCommunicator


class UserService:
    def __init__(self, user_communicator: IUserCommunicator):
        self.__user_comm = user_communicator

    def add_user(self):
        try:
            user_as_json = request.json
            user = User.create_from_json(user_as_json)
            self.__user_comm.upload(user)
            return MessageHandler.get_success_msg(f"Successful adding user {user.id}")
        except UserAlreadyExistsError as e:
            return MessageHandler.get_error_msg(str(e)), 302
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

    def delete_user(self, user_id: str):
        if request.method == "DELETE":
            try:
                self.__user_comm.delete(user_id)
                return MessageHandler.get_success_msg(f"Successfully deleted {user_id}")
            except UserNotFoundError as e:
                return MessageHandler.get_error_msg(str(e)), 404
            except Exception as e:
                return MessageHandler.get_error_msg(str(e)), 400
        else:
            MessageHandler.get_error_msg("Something went wrong"), 400
