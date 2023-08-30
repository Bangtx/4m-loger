
create table sensor (
	id bigint NOT NULL IDENTITY PRIMARY KEY,
	name text,
-- 	host text,
	port text,
	unit int,
	machine_id int default 1,
	position text,
);


create table temperature (
	id bigint NOT NULL IDENTITY PRIMARY KEY,
	temp float,
	sensor_id bigint FOREIGN KEY REFERENCES sensor(id),
	status int,
	datetime datetime default CURRENT_TIMESTAMP
);


insert into sensor (name, port ,unit)
values ('sensor 1', '192.168.1.254', 8880, 1),
       ('sensor 2', '192.168.1.254', 8880, 2)