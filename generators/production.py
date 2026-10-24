import random 
from datetime import datetime, timedelta

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

def generate_production_datetime(start_datetime):
    
    delay_times_minutes = [0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 10, 20, 30, 40]
    delay_weights = [950, 420, 190, 140, 100, 80, 60, 40, 30, 20, 7, 3, 2, 1]

    interval = 2
    pauses = [
        (1, 20, 1, 30),
        (2, 50, 3, 0),
        (4, 20, 4, 30), 
        (9, 0, 9, 15),
        (11, 45, 12, 15),
        (18, 15, 18, 45),
        (21, 30, 21, 45)
    ]

    end_datetime = start_datetime + timedelta(days = 1)

    times = []
    current_datetime = start_datetime

    while current_datetime < end_datetime: 
        times.append(current_datetime)

        delay = random.choices(delay_times_minutes, delay_weights, k = 1)[0]

        next_datetime = current_datetime + timedelta(minutes = interval + delay)

        for (start_hour, start_minute, end_hour, end_minute) in pauses:
                pause_start = current_datetime.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)
                pause_end = current_datetime.replace(hour=end_hour, minute=end_minute, second=0, microsecond=0)
        
                if pause_start <= next_datetime < pause_end:
                    next_datetime = pause_end 
                    break 
        current_datetime = next_datetime

    return times     

  

def generate_production(igef_start_number, start_datetime):
    line_1_times = sorted(generate_production_datetime(start_datetime))
    line_2_times = sorted(generate_production_datetime(start_datetime))
    # sorted - Absicherung, normalerweise nicht notwendig
    number_of_cars = len(line_1_times) + len(line_2_times)
    igefs = generate_igef(number_of_cars, igef_start_number)
    models = generate_models(number_of_cars)

    lines = []
    datetimes = []

    i = 0 
    j = 0 


    while i < len(line_1_times) or j < len(line_2_times):

        if i >= len(line_1_times):
            # Linie 1 ist fertig, keine Fahrzeuge mehr 
            lines.append(2)
            datetimes.append(line_2_times[j])
            j += 1
        
        elif j>= len(line_2_times):
            # Linie 2 ist fertig
            lines.append(1)
            datetimes.append(line_1_times[i])
            i += 1
        
        elif line_1_times[i] <= line_2_times[j]:
            # Chronologisch; Zeit vergleichen; 
            lines.append(1)
            datetimes.append(line_1_times[i])
            i += 1 
        
        else:
            lines.append(2)
            datetimes.append(line_2_times[j])
            j += 1 
         
         
    return igefs, models, lines, datetimes