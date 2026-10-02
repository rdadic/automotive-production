CREATE TRIGGER UpdateVehicleStatus 
AFTER INSERT ON production FOR EACH ROW 
INSERT INTO vehicle_status(igef, location, datetime)
VALUES (NEW.igef, CONCAT('Lackiererei, UBS line ', NEW.ubs_line), NOW());