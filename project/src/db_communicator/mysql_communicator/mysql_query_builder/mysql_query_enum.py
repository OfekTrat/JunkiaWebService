from enum import Enum


class MySQLQueries(Enum):
    UPLOAD_FINDING = "INSERT INTO `junkia`.`findings` (id, longitude, latitude, image_hash, tags) " \
                     "VALUES ('{finding_id}', '{longitude}', '{latitude}', '{image_hash}', '{tags}');"
    GET_FINDING = "SELECT * FROM `junkia`.`findings` WHERE id = '{finding_id}'"
    DELETE_FINDING = "DELETE FROM `junkia`.`findings` WHERE id = '{finding_id}'"
    RADIUS_SEARCH = "SELECT * FROM `junkia`.`findings`" \
                    "WHERE POW(longitude - {longitude}, 2) + POW(latitude - {latitude}, 2) <= POW({radius}, 2)"

    ADD_USER = "INSERT INTO `junkia`.`users` (id, tags, longitude, latitude, radius, last_notified) " \
               "VALUES ('{userid}', '{tags}', '{longitude}', '{latitude}', '{radius}', '{last_notified}');"
    GET_USER = "SELECT * FROM `junkia`.`users` WHERE id = '{user_id}'"
    UPDATE_USER = "UPDATE `junkia`.`users`" \
                  "SET" \
                  " tags = '{tags}'," \
                  " longitude = '{longitude}'," \
                  " latitude = '{latitude}'," \
                  " radius = '{radius}'" \
                  "WHERE id = '{user_id}'"
