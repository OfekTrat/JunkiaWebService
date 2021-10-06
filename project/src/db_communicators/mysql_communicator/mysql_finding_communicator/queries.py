from enum import Enum


class Queries(Enum):
    GET = "SELECT * FROM junkia.findings WHERE id = '{finding_id}'"
    UPLOAD = "INSERT INTO junkia.findings (id, longitude, latitude, image_hash, tags) " \
             "VALUES ('{finding_id}', {longitude}, {latitude}, '{image_hash}', '{tags}')"
    DELETE = "DELETE FROM junkia.findings WHERE id IN ({ids})"
    FIND_BY_RADIUS = "SELECT * FROM junkia.findings " \
                     "WHERE ST_DISTANCE_SPHERE(POINT({longitude}, {latitude}), POINT(longitude, latitude)) " \
                     "<= {radius} * 1000"
