DROP INDEX IF EXISTS idx_production_igef;

CREATE INDEX idx_production_igef ON production(igef);

DROP INDEX IF EXISTS idx_production_model;
CREATE INDEX idx_production_model ON production(model);

DROP INDEX IF EXISTS idx_measurements_igef; 
CREATE INDEX idx_measurements_model ON production_measurements(igef);