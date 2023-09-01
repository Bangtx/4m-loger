CREATE TABLE IF NOT EXISTS machine
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id INTEGER,
    name TEXT,
    position TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    modified_at TIMESTAMP,
    modified_by INTEGER,
    deleted_at TIMESTAMP,
    deleted_by INTEGER,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS sensor (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name text,
    address int,
	machine_id int,
	type text,
	position text,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    modified_at TIMESTAMP,
    modified_by INTEGER,
    deleted_at TIMESTAMP,
    deleted_by INTEGER,
    active BOOLEAN DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS parameter
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER,
    machine_id INTEGER,
    temperature_1 REAL,
    temperature_2 REAL,
    temperature_3 REAL,
    temperature_4 REAL,
    current REAL,
    date DATE,
    time TIME,
    is_running BOOLEAN DEFAULT FALSE,
    is_problem BOOLEAN DEFAULT FALSE,
    is_uploaded BOLLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    modified_at TIMESTAMP,
    modified_by INTEGER,
    deleted_at TIMESTAMP,
    deleted_by INTEGER,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS setting
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key text,
    value text,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    modified_at TIMESTAMP,
    modified_by INTEGER,
    deleted_at TIMESTAMP,
    deleted_by INTEGER,
    active BOOLEAN DEFAULT TRUE
);


insert into setting (key, value)
values ('method', 'rtu'),
       ('port', 'COM4'),
       ('baudrate', '57600')
       ('company', '2');


insert into machine (server_id, name, position)
VALUES
    (null, 'cnc 1', null),
    (null, 'cnc 2', null),
    (null, 'cnc 3', null),
    (null, 'cnc 4', null);

insert into sensor (name, adress, machine_id, position, type)
values
    ('cnc electric current 1', 16, 1, null, 'current'),
    ('cnc electric current 2', 17, 1, null, 'current'),
    ('cnc electric current 3', 18, 1, null, 'current'),
    ('cnc electric current 4', 19, 1, null, 'current');