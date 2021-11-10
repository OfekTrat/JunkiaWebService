from models import Image
from flask import request
from views.message_handler import MessageHandler
from communicators.interfaces import IImageCommunicator
from .exceptions import ImageNotFoundError, ImageAlreadyExistsError


class ImageService:
    def __init__(self, image_communicator: IImageCommunicator):
        self.__image_comm = image_communicator

    def get_image(self, image_hash: str):
        try:
            image = self.__image_comm.get(image_hash)
            return MessageHandler.get_data_msg(image.to_json())
        except ImageNotFoundError as e:
            return MessageHandler.get_error_msg("File Not Found"), 404
        except Exception as e:
            return MessageHandler.get_error_msg(str(e)), 400

    def upload_image(self):
        if request.method == "POST":
            try:
                image = Image.from_json(request.json)
                self.__image_comm.upload(image)
                return MessageHandler.get_success_msg("Successful Image Upload")
            except ImageAlreadyExistsError as e:
                return MessageHandler.get_error_msg("Image Already Exists"), 302
        else:
            return MessageHandler.get_error_msg("Something went wrong"), 400

    def delete_image(self):
        if request.method == "DELETE":
            try:
                print(request)
                hashes_to_delete = request.json["hashes"]
                self.__image_comm.delete_multiple(hashes_to_delete)
                return MessageHandler.get_success_msg("Successful Delete")
            except Exception as e:
                return MessageHandler.get_error_msg(str(e)), 400
        else:
            return MessageHandler.get_error_msg("Something went wrong"), 400
