

'''
CREATE DATABASE IF NOT EXISTS automotive_production; 
USE DATABASE automotive_production;

CREATE TABLE models(
    model_id INT NOT NULL, 
    model VARCHAR(10) NOT NULL, 
    drive_type VARCHAR(10) NOT NULL, 
    PRIMARY KEY(vehicle_id)
); 

INSERT INTO models(model_id, model, drive_type) VALUES
(1,'G20','ICE'),
(2,'G20, 'PHEV'),
(3,'G21','ICE'),
(4,'G21','PHEV'),
(5,'G26','BEV'),
(6,'G26','ICE'),
(7,'G80','ICE'),
(8,'G81','ICE');

df = pd.read_csv('path') 
sql = """
    INSERT INTO models(model_id, model, drive_type) VALUES (%s, %s, %s)
"""

for row in df.itertuples(index=False):
    cursor.execute(sql, (row.model_id, row.model, row.drive_type))

connection.commit() 

CREATE TABLE robot_types(
    robot_number INT NOT NULL PRIMARY KEY, 
    process_area  VARCHAR(255) NOT NULL
);

INSERT INTO robot_types(robot_number, process_area) VALUES
(11,'Batteriekasten'),
(12,'Getriebetunnel'),
(21,'Radhaus hinten links'),
(22,'Radhaus hinten rechts'),
(31, 'Schweller links'),
(32, 'Schweller rechts'),
(41, 'Foerderbereich links'),
(42, 'Foerderbereich rechts');



CREATE TABLE robots(
    robot_id INT NOT NULL PRIMARY KEY,
    robot_number INT NOT NULL,
    ubs_line INT NOT NULL, 
    FOREIGN KEY(robot_number) REFERENCES robot_types(robot_number) 
    ON DELETE CASACE 
    ON UPDATE CASCADE
);

INSERT INTO robots VALUES(robot_id robot_number, ubs_line, process_area) VALUES
(1, 11, 1),
(2, 12, 1),
(3, 21, 1),
(4, 22, 1),
(5, 31, 1),
(6, 32, 1),
(7, 41, 1),
(8, 42, 1),
(9, 11, 2),
(10, 12, 2),
(11, 21, 2),
(12, 22, 2),
(13, 31, 2),
(14, 32, 2),
(15, 41, 2),
(16, 42, 2);

 
CREATE TABLE process_specifications(
    specification_id INT NOT NULL PRIMARY KEY, 
    model_id INT NOT NULL, 
    robot_number INT NOT NULL, 
    target_area_cm2 DECIMAL(8,2) NOT NULL,
    target_thickness_mm DECIMAL(6,2) NOT NULL, 
    target_volume_ml DECIMAL(5,2) NOT NULL,
    FOREIGN KEY(model_id) REFERENCES models(model_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(robot_number) REFERENCES robot_types(robot_number)  
);

import pandas as pd 

df = pd.read_excel('path', header = 0)
specification_ids = df["specification_id"].tolist()
model_ids = df["model_id"].tolist()
robot_numbers = df["robot_number"].tolist()
target_areas = df["target_area_cm2"].tolist()
target_volumes = df["target_volume_ml"].tolist()
target_mm = df["target_thickness_mm"].tolist()

specifications_insert = """
INSERT INTO process_specifications
(specifications_id, model_id, robot_number, target_area_cm2,
target_thickness_mm, target_volume_ml) 
VALUES (%s, %s, %s, %s, %s)
"""

for specification_id, model_id, robot_number, target_area, target_thickness, target_volume in zip(specifications_ids, model_ids, robot_numbers, target_areas, target_mm, target_volumes):
    cursor.execute(specifictions_insert, (specification_id, model_id, robot_number, target_area, target_thickness, target_volume))

connection.commit()

CREATE TABLE production(
    igef VARCHAR(255) NOT NULL PRIMARY KEY, 
    model_id INT NOT NULL, 
    ubs_line INT NOT NULL, 
    production_datetime DATETIME NOT NULL, 
    FOREIGN KEY(model_id) REFERENCES models(model_id) ON DELETE CASCADE ON UPDATE CASCADE
);

!!! datetime - paziti na takt 2 min 

('IGEF00000001', 1, 1, '2026-09-15 05:56:13'),
('IGEF00000002', 2, 2, '2026-09-15 05:56:11'),
('IGEF00000003', 3, 1, '2026-09-15 05:58:17'),
('IGEF00000004', 4, 2, '2026-09-15 05:58:13'),
('IGEF00000005', 5, 1, '2026-09-15 06:00:11'),
('IGEF00000006', 6, 2, '2026-09-15 06:00:34'),
('IGEF00000007', 7, 2, '2026-09-15 06:02:40'),
('IGEF00000008', 8, 1, '2026-09-15 06:02:05'),
('IGEF00000009', 1, 2, '2026-09-15 06:04:40'),
('IGEF00000010', 5, 2, '2026-09-15 06:06:42'),
('IGEF00000011', 3, 1, '2026-09-15 06:04:28'),
('IGEF00000012', 4, 1, '2026-09-15 06:06:31'),

 

CREATE TABLE production_measurements(
    measurement_id INT NOT NULL AUTO INCREMENT PRIMARY KEY,
    igef VARCHAR(255) NOT NULL,
    specification_id INT NOT NULL,  #POMOCU MODELA ODREDITI 
    robot_id INT NOT NULL,  #pomocu linije 1-8 9-16
    actual_ml DECIMAL(5,2) NOT NULL,  #random
    deviation_prozent DECIMAL(5,2), 
    requires_inspection BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(igef) REFERENCES production(igef) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(specification_id) REFERENCES process_specifications(specification_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(robot_id) REFERENCES robots(robot_id)
);


CREATE TABLE vehicle_status(
    igef VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL
);


'''