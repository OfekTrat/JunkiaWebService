from flask import Flask
from abc import ABC, abstractmethod
from services.iservice import IService


class AppInitializer(ABC):
    @classmethod
    def _create_app(cls) -> Flask:
        return Flask(__name__)

    @classmethod
    @abstractmethod
    def get_app(cls, service: IService) -> Flask:
        raise NotImplementedError()
