from flask import Flask
from .app_initializer_abs import AppInitializer
from services.finding_service import FindingService


class FindingAppInitializer(AppInitializer):
    @classmethod
    def get_app(cls, finding_service: FindingService) -> Flask:
        app = cls._create_app()
        app.add_url_rule("/finding/<finding_id>", methods=["GET"], view_func=finding_service.get_finding)
        app.add_url_rule("/finding/<finding_id>", methods=["DELETE"], view_func=finding_service.delete_finding)
        app.add_url_rule("/finding/by_radius", methods=["POST"], view_func=finding_service.get_finding_by_radius)
        app.add_url_rule("/finding", methods=["POST"], view_func=finding_service.upload_finding)
        return app
