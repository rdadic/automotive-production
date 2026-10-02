'''


def generate_number_of_cars():
    
    limit_day_shifts = 420 
    limit_night_shift = 310

    production_day = [410, 400, 375, 360, 350, 340, 320, 300, 280, 250, 240, 220, 210, 190, 180, 160, 140, 110]
    weights_day = [11, 13, 15, 15, 10, 8, 6, 6, 5, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2,1]
    production_night = [310, 305, 300, 290, 280, 270, 260, 250, 240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140, 120, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    weights_night = [1, 2, 4, 5, 6, 6, 6, 7, 7, 8, 8, 10, 10, 10, 11, 10, 12, 7, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1 ,1]

    morning_base = random.choices(production_day, weights = weight_day, k=1)[0]
    morning_production = morning_base + random.randint(-4,3)

    afternoon_base = random.choices(production_day, weights = weight_day, k=1)[0]
    afternoon_production = afternoon_base + random.randint(-4,3)

    night_base = random.choices(production_night, weights = weights_night, k=1)[0]
    night_production = night_base + random.randint(-4,3)

    produced = night_production + morning_production + afternoon_production

    return produced

def generate_igef(number_cars, start_number):
    igefs = []
    for i in range(start_number, start_number + number_cars):
        igef = 'IGEF' + str(i).zfill(8)
        igefs.append(igef)

    return igefs

def generate_models(number_of_cars):
    models_number = [1, 2, 3, 4, 5, 6, 7, 8]
    weights_models = [60, 2, 75, 5, 142, 68, 15, 13]
     
    models = random.choices(models_number, weights_models, k= number_of_cars)[0]

    return models

def ubs_line(number_of_cars):
    lines = [1, 2]
    lines_weights = [50, 50]

    return random.choices(lines, weights = lines_weights, k = number_of_cars)


from datetime import datetime, timedelta

def generate_production_datetime(number_cars, start_datetime):
    datetimes = []
    current_datetime = start_datetime 

    delay_times_minutes = [0, 0.5, 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 25, 30, 45, 60, 70, 80]
    delay_weights = [180, 175, 170, 160, 120, 110, 105, 100, 95, 70, 52, 45, 40, 26, 11, 7, 5, 3]

    interval = 2

    pauses = [
        (9, 0, 9, 15),
        (11, 45, 12, 15),
        (18, 15, 18, 45),
        (21, 30, 21, 45)
    ]

    for i in range(number_cars):
        
        datetimes.append(current_datetime)
        delay = random.choices(delay_times_minutes, weights = delay_weights, k = 1)[0]

        next_datetime = current_datetime + timedelta(minutes = interval + delay)

        for start_hour, start_minute, end_hour, end_minute in pauses:
            pause_start = current_datetime.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
            pause_end = current_datetime.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
        
        if pause_start <= next_datetime < pause_end:
            next_datetime = pause_end 
            break #break se vrati gore u i petlju, ne ide dolje na current_time
            # 9 i 20 moze, jer nema <= vec samo <
        
        current_datetime = next_datetime
    
    return datetimes

def generate_production(igef_start_number, start_datetime):
    number_of_cars = generate_number_of_cars() 
    igefs = generate_igef(number_of_cars, igef_start_number)
    models = generate_models(number_of_cars)
    lines = generate_lines(number_of_cars)
    datetimes = generate_production_datetime(number_of_cars, start_datetime)

    return igefs, models, lines, datetimes

igefs, models, lines, datetimes = generate_production(1, datetime(2026,9,23,0,0))

production_data = list(zip(igefs, models, lines, datetimes))

sql = """INSERT INTO production(igef,model_id, ubs_line, production_datetime) 
VALUES (%s, %s, %s, %s)
"""

cursor.executemany(sql, production_data)
connection.commit()



def generate_production_measuremnets():
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
                (igef, specification_id, robot_id, actual_ml, deviation_ml, requires_inspection)
            )
        
    return measurements

    
def generate_actual_volume(target_volume_ml):
    deviations = [-100, -90, -80, -70, -50, -40, -30, -20, -10, 0, 5, 10, 15, 20, 30, 50, 60, 70, 80, 100, 150, 200]
    weights = [40, 40, 30, 30, 20, 15, 15, 55, 90, 95, 90, 95, 80, 70, 60, 10, 1, 1, 1, 1, 5, 5]

    deviation = random.choices(deviations, weights = weights, k=1)[0]

    actual_ml = target_volume_ml + deviation

    return round(actual_ml, 2)



'''