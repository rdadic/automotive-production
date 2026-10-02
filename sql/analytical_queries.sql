
USE automotive_production; 

SELECT m.model, COUNT(*) AS quantity 
FROM production p 
INNER JOIN models m 
    ON p.model_id = m.model_id
GROUP BY m.model WITH ROLLUP;

PREPARE GetMeasurementsDetail FROM 'SELECT specification_id, robot_id, actual_ml,
                deviation_prozent, requires_inspection FROM production_measurements 
                WHERE igef=?';

SET @igef = ''; 
EXECUTE GetMeasurementsDetail USING @igef;


WITH 
production_data AS (SELECT model_id, COUNT(*) AS value FROM production_data
                    GROUP BY model_id),
pvc_data AS (SELECT p.model_id, SUM(pm.actual_ml) AS value FROM production AS p
                INNER JOIN production_measurements AS pm ON p.igef = pm.igef)

SELECT m.model, "Vehicles made" AS metric, pd.value FROM production_data AS pd 
        INNER JOIN models AS m ON m.model_id = pd.model_id
UNION
SELECT m.model, "PVC used (liters)" AS metric, pvc.value FROM pvc_data AS pvc
        INNER JOIN models AS m ON m.models_id = pvc.model_id

ORDER BY model, metric;

SELECT robot_id, COUNT(*) AS inspection_count 
FROM production_measurements 
WHERE requieres_inspection = TRUE 
GROUP BY robot_id 
HAVING COUNT(*) > (SELECT AVG(inspection_count) FROM
(
        SELECT robot_id, COUNT(*) AS inspection_count FROM production_measurements
        WHERE requires_inspection = TRUE
        GROUP BY robot_id 
) AS robots_temp
)
ORDER BY inspection_count DESC;





































