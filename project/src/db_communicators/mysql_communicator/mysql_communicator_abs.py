from typing import List


class MySQLCommunicatorAbs:
    @classmethod
    def _tags_to_str(cls, tags: List[str]) -> str:
        return ",".join(tags)

    @classmethod
    def _str_to_tags(cls, tags_as_str: str) -> List[str]:
        return tags_as_str.split(",")
