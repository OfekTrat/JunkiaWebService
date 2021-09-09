from typing import Any, List

from .mysql_query_enum import MySQLQueries
from project.src.finding import Finding
from project.src.location import Location
from project.src.user import User


class MySQLQueryBuilder:
    @classmethod
    def build_upload_finding(cls, finding: Finding) -> str:
        return MySQLQueries.UPLOAD_FINDING.value.format(
            finding_id=finding.id,
            longitude=finding.location.longitude,
            latitude=finding.location.latitude,
            image_hash=finding.image_hash,
            tags=cls.__convert_list_to_string(finding.tags)
        )

    @staticmethod
    def build_get_finding(finding_id: str) -> str:
        return MySQLQueries.GET_FINDING.value.format(finding_id=finding_id)

    @staticmethod
    def build_delete_finding(finding_id: str) -> str:
        return MySQLQueries.DELETE_FINDING.value.format(finding_id=finding_id)

    @staticmethod
    def build_radius_finding_search(location: Location, radius: int) -> str:
        return MySQLQueries.RADIUS_SEARCH.value.format(longitude=location.longitude,
                                                       latitude=location.latitude,
                                                       radius=radius)

    @classmethod
    def build_add_user(cls, user: User) -> str:
        return MySQLQueries.ADD_USER.value.format(
            userid=user.id,
            tags=cls.__convert_list_to_string(user.tags),
            longitude=user.location.longitude,
            latitude=user.location.latitude,
            radius=user.radius,
            last_notified=user.last_notified)

    @staticmethod
    def build_get_user(user_id: str) -> str:
        return MySQLQueries.GET_USER.value.format(user_id=user_id)

    @classmethod
    def build_update_user(cls, updated_user: User) -> str:
        return MySQLQueries.UPDATE_USER.value.format(
            tags=cls.__convert_list_to_string(updated_user.tags),
            longitude=updated_user.location.longitude,
            latitude=updated_user.location.latitude,
            radius=updated_user.radius,
            user_id=updated_user.id
        )

    @staticmethod
    def __convert_list_to_string(lst: List[Any]) -> str:
        return ",".join(lst)
