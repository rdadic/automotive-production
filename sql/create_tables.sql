CREATE DATABASE IF NOT EXISTS automotive_production;

USE automotive_production;

CREATE TABLE models(
    model_id INT NOT NULL, 
    model VARCHAR(10) NOT NULL, 
    drive_type VARCHAR(10) NOT NULL, 
    PRIMARY KEY(model_id)
); 

CREATE TABLE robot_types(
    robot_number INT NOT NULL PRIMARY KEY, 
    process_area VARCHAR(255) NOT NULL
);

CREATE TABLE robots(
    robot_id INT NOT NULL PRIMARY KEY,
    robot_number INT NOT NULL,
    ubs_line INT NOT NULL, 
    FOREIGN KEY(robot_number) REFERENCES robot_types(robot_number) 
    ON DELETE CASCADE 
    ON UPDATE CASCADE
);

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

CREATE TABLE production(
    igef VARCHAR(255) NOT NULL PRIMARY KEY, 
    model_id INT NOT NULL, 
    ubs_line INT NOT NULL, 
    production_datetime DATETIME NOT NULL, 
    FOREIGN KEY(model_id) REFERENCES models(model_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE production_measurements(
    measurement_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    igef VARCHAR(255) NOT NULL,
    specification_id INT NOT NULL,  
    robot_id INT NOT NULL,  
    actual_ml DECIMAL(5,2) NOT NULL, 
    deviation_percent DECIMAL(5,2), 
    requires_inspection BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY(igef) REFERENCES production(igef) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(specification_id) REFERENCES process_specifications(specification_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(robot_id) REFERENCES robots(robot_id)
);

CREATE TABLE vehicle_status(
    igef VARCHAR(255) NOT NULL,
    vehicle_location VARCHAR(255) NOT NULL,
    date_time DATETIME NOT NULL
);


