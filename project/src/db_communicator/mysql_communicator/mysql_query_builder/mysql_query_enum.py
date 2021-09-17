from enum import Enum


class MySQLQueries(Enum):
    UPLOAD_FINDING = "INSERT INTO `junkia`.`findings` (id, longitude, latitude, image_hash, tags) " \
                     "VALUES ('{finding_id}', '{longitude}', '{latitude}', '{image_hash}', '{tags}');"
    GET_FINDING = "SELECT * FROM `junkia`.`findings` WHERE id = '{finding_id}'"
    DELETE_FINDING = "DELETE FROM `junkia`.`findings` WHERE id = '{finding_id}'"
    RADIUS_SEARCH = """select * from junkia.findings
                       where 2 * atan2(
		                             sqrt(
			                             (sin((latitude-{latitude}) / 2)) ^ 2 + cos(latitude) * cos({latitude}) *
				                         (sin((longitude - {longitude}) / 2)) ^ 2
			                         ),
			                         sqrt(
			                             1-((sin((latitude-{latitude}) / 2)) ^ 2 + cos(latitude) * cos({latitude}) *
                                         (sin((longitude - {longitude}) / 2))) ^ 2
                                     )
		                         ) <= {radius}"""

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
