FROM mysql

COPY ./mysql_data /docker-entrypoint-initdb.d/

EXPOSE 3306
