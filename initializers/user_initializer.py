from flask import Flask
from .app_initializer_abs import AppInitializer
from services.user_service import UserService


class UserAppInitializer(AppInitializer):
    @classmethod
    def get_app(cls, user_service: UserService) -> Flask:
        app = cls._create_app()
        app.add_url_rule("/user", methods=["POST"], view_func=user_service.add_user)
        app.add_url_rule("/user/<user_id>", methods=["GET"], view_func=user_service.get_user)
        app.add_url_rule("/user/<user_id>", methods=["PUT"], view_func=user_service.update_user)
        app.add_url_rule("/user/<user_id>", methods=["DELETE"], view_func=user_service.delete_user)
        return app
