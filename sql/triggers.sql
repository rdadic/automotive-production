CREATE TRIGGER UpdateVehicleStatus 
AFTER INSERT ON production FOR EACH ROW 
INSERT INTO vehicle_status(igef, vehicle_location, date_time)
VALUES (NEW.igef, CONCAT('Lackiererei, UBS line ', NEW.ubs_line), NEW.production_datetime);