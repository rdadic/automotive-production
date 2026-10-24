DROP VIEW IF EXISTS models_made_view;

CREATE VIEW models_made_view AS 
SELECT model, COUNT(*) AS quantity FROM production
INNER JOIN models ON production.model_id = models.model_id
GROUP BY model;

SELECT * FROM models_made_view;

DROP VIEW IF EXISTS production_by_line_view;

CREATE VIEW production_by_line_view AS 
SELECT ubs_line AS "UBS Line", COUNT(*) AS 'Quantity' FROM production 
GROUP BY ubs_line;

SELECT * FROM production_by_line_view;


DROP VIEW IF EXISTS quality_overview_view;

CREATE VIEW quality_overview_view AS 
SELECT 
    COUNT(*) AS total_measurements_places,
    SUM(requires_inspection) as inspections, 
    AVG(ABS(deviation_percent)) AS avg_abs_deviation_percent
FROM production_measurements; 

SELECT * FROM quality_overview_view;
