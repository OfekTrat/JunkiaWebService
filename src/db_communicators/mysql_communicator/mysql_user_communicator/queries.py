from enum import Enum


class Queries(Enum):
    GET = "SELECT * FROM junkia.users WHERE id = '{user_id}';"
    DELETE = "DELETE FROM junkia.users WHERE id = '{user_id}';"
    UPLOAD = "INSERT INTO junkia.users (id, tags, longitude, latitude, radius, last_notified) " \
             "VALUES ('{user_id}', '{tags}', '{longitude}', '{latitude}', '{radius}', '{last_notified}');"
    UPDATE = "UPDATE `junkia`.`users` SET tags = '{tags}', longitude = '{longitude}', latitude = '{latitude}'," \
                  " radius = '{radius}' WHERE id = '{user_id}'"
