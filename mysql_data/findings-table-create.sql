CREATE TABLE junkia.findings (id CHAR(15), longitude FLOAT, latitude FLOAT, image_hash VARCHAR(256), tags VARCHAR(1000), PRIMARY KEY (id));
insert into junkia.findings (id, longitude, latitude, image_hash, tags) value ('test', 1, 1, 'asdfgh', 'tag1,tag2');
