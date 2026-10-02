import random 
from datetime import datetime, timedelta


def generate_number_of_cars():
    
    limit_day_shifts = 420 
    limit_night_shift = 310

    production_day = [410, 400, 375, 360, 350, 340, 320, 300, 280, 250, 240, 220, 210, 190, 180, 160, 140, 110, 90, 70, 60, 50, 30, 20]
    weights_day =[100, 120, 145, 135, 130, 110, 80, 65, 54, 50, 47, 42, 35, 32, 28, 24, 20, 16, 14, 12, 10, 8, 4, 3]
    production_night = [310, 305, 300, 290, 280, 270, 260, 250, 240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140, 120, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    weights_night = [1, 2, 4, 5, 6, 6, 6, 7, 7, 8, 8, 10, 10, 10, 11, 10, 12, 7, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 1, 1 ,1]

    morning_base = random.choices(production_day, weights = weights_day, k=1)[0]
    morning_production = morning_base + random.randint(-4,3)

    afternoon_base = random.choices(production_day, weights = weights_day, k=1)[0]
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
     
    models = random.choices(models_number, weights_models, k= number_of_cars)

    return models

def generate_lines(number_of_cars):
    lines = [1, 2]
    lines_weights = [50, 50]

    return random.choices(lines, weights = lines_weights, k = number_of_cars)


def generate_production_datetime(lines, start_datetime):
    datetimes = []
    

    delay_times_minutes = [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 10]
    delay_weights = [180, 175, 170, 160, 120, 110, 80, 60, 40, 20, 10]

    interval = 120

    end_datetime = start_datetime + timedelta(days = 1)

    pauses = [
        (9, 0, 9, 15),
        (11, 45, 12, 15),
        (18, 15, 18, 45),
        (21, 30, 21, 45)
    ]

    line_datetimes = {
        1: [],
        2: []
    }

    for line in [1, 2]:
        current_datetime = start_datetime

        number_of_cars = lines.count(line)  

        for car in range(number_of_cars):
            line_datetimes[line].append(current_datetime)

            delay = random.choices(delay_times_minutes, delay_weights, k=1)[0]
            
            next_datetime = current_datetime + timedelta(seconds = interval + delay*60)

            for (start_hour, start_minute, end_hour, end_minute) in pauses:
                pause_start = current_datetime.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
                pause_end = current_datetime.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
        
                if pause_start <= next_datetime < pause_end:
                    next_datetime = pause_end 
                    break 
            
            

            if next_datetime >= end_datetime:
                break

            current_datetime = next_datetime
                

            

    counters = {
        1:0,
        2:0
    }

    for line in lines: 
        datetimes.append(line_datetimes[line][counters[line]])
        counters[line] += 1
    
    return datetimes

def generate_production(igef_start_number, start_datetime):
    number_of_cars = generate_number_of_cars() 
    igefs = generate_igef(number_of_cars, igef_start_number)
    models = generate_models(number_of_cars)
    lines = generate_lines(number_of_cars)
    datetimes = generate_production_datetime(lines, start_datetime)

    return igefs, models, lines, datetimes