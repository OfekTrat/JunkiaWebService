from flask import Flask
from services.finding_service import FindingService
from services.user_service import UserService
from services.image_service import ImageService


class AppInitializer:
    def __init__(self):
        self.__app = Flask(__name__)

    def add_finding_service(self, finding_service: FindingService):
        self.__app.add_url_rule("/finding/<finding_id>", methods=["GET"], view_func=finding_service.get_finding)
        self.__app.add_url_rule("/finding/<finding_id>", methods=["DELETE"], view_func=finding_service.delete_finding)
        self.__app.add_url_rule("/finding/by_radius", methods=["POST"], view_func=finding_service.get_finding_by_radius)
        self.__app.add_url_rule("/finding", methods=["POST"], view_func=finding_service.upload_finding)

    def add_user_service(self, user_service: UserService):
        self.__app.add_url_rule("/user", methods=["POST"], view_func=user_service.add_user)
        self.__app.add_url_rule("/user/<user_id>", methods=["GET"], view_func=user_service.get_user)
        self.__app.add_url_rule("/user/<user_id>", methods=["PUT"], view_func=user_service.update_user)
        self.__app.add_url_rule("/user/<user_id>", methods=["DELETE"], view_func=user_service.delete_user)

    def add_image_service(self, image_service: ImageService):
        self.__app.add_url_rule("/image/<image_hash>", methods=["GET"], view_func=image_service.get_image)
        self.__app.add_url_rule("/image", methods=["POST"], view_func=image_service.upload_image)
        self.__app.add_url_rule("/image", methods=["DELETE"], view_func=image_service.delete_image)

    def get_app(self) -> Flask:
        return self.__app

