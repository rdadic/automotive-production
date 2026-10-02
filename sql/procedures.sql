
DROP PROCEDURE IF EXISTS DailyPVCAmount; 

DELIMITER // 
CREATE PROCEDURE DailyPVCAmount(IN production_date_input DATE, OUT pvc_liter DECIMAL(6,2))
BEGIN 
SELECT SUM(pm.actual_ml)/1000 INTO pvc_liter FROM production_measurements AS pm
INNER JOIN production AS p 
ON pm.igef = p.igef 
WHERE DATE(production.production_datetime) = production_date_input;
END  // 

DELIMITER ; 

SET @pvc_liter; 
CALL DailyPVCAmount('2026-09-21', @pvc_liter);
SELECT @pvc_liter;

DROP PROCEDURE IF EXISTS DailyShiftReport;

DELIMITER // 
CREATE PROCEDURE DailyShiftReport(production_date_input DATETIME)
BEGIN 
    WITH shift_data AS (
        SELECT
            CASE
                WHEN TIME(production_datetime) > '05:50:00' AND TIME(production_datetime) <= '14:55:00'
                THEN 'Morning'
                WHEN TIME(production_datetime) > '14:55:00' AND TIME(production_datetime) <= '23:59:00'
                THEN 'Afternoon'
                ELSE 'Night' 
            END AS 'shift'
        FROM production 
        WHERE DATE(production_datetime) = production_date_input
    )
    
    SELECT shift, COUNT(*) AS quantity FROM shift_data
    GROUP BY shift
    ORDER BY field(shift, 'Night', 'Morning', 'Afternoon');

END // 

DELIMITER ;

CALL DailyShiftReport('2026-09-21');