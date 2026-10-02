import random 

def generate_production_measurements(cursor):
    sql = """
        SELECT igef, model_id, ubs_line FROM production ORDER BY production_datetime
    """
    cursor.execute(sql)
    production_data = cursor.fetchall()

    measurements = []

    for igef, model, ubs_line in production_data: 
        sql = """SELECT specification_id, robot_number, target_volume_ml FROM process_specifications 
                WHERE model_id = %s"""
        cursor.execute(sql, (model,))
        specifications = cursor.fetchall()

        for specification_id, robot_number, target_volume_ml in specifications:
            if ubs_line == 1:
                robot_id = {
                    11:1, 
                    12:2,
                    21:3,
                    22:4,
                    31:5,
                    32:6,
                    41:7, 
                    42:8
                }[robot_number]
            else: 
                robot_id = {
                    11:9,
                    12:10,
                    21:11,
                    22:12,
                    31:13,
                    32:14,
                    41:15,
                    42:16
                }[robot_number]

            actual_ml = generate_actual_volume(target_volume_ml)
            deviation_ml = actual_ml - target_volume_ml 

            deviation_percent = (deviation_ml / target_volume_ml) * 100 

            requires_inspection = abs(deviation_percent) >= 5


            
            measurements.append(
                (igef, specification_id, robot_id, actual_ml, deviation_percent, requires_inspection)
            )
        
    return measurements

    
def generate_actual_volume(target_volume_ml):
    deviations = [-100, -90, -80, -70, -50, -40, -30, -20, -10, 0, 5, 10, 15, 20, 30, 50, 60, 70, 80, 100, 150, 200]
    weights = [40, 40, 30, 30, 20, 15, 15, 160, 180, 190, 180, 165, 150, 70, 60, 10, 5, 5, 5, 5, 6, 7]

    deviation = random.choices(deviations, weights = weights, k=1)[0]

    actual_ml = target_volume_ml + deviation

    return round(actual_ml, 2)



