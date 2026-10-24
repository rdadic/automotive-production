import mysql.connector as connector
from mysql.connector import errorcode
import pandas as pd 
import generators
from datetime import datetime
from dotenv import load_dotenv
import os 
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")


connection = connector.connect(
    host = os.environ["MYSQL_HOST"],
    port = int(os.getenv("MYSQL_PORT","3306")),
    user= os.environ["MYSQL_USER"],
    password = os.environ["MYSQL_PASSWORD"],
    database = os.environ["MYSQL_DATABASE"]
)

cursor = connection.cursor()

models_df = pd.read_csv('data/models.csv')
robots_df = pd.read_csv('data/robots.csv')
robot_types_df = pd.read_csv('data/robot_types.csv')
specifications_df = pd.read_excel('data/specifications.xlsx')


date = datetime(2026, 9, 21, 0, 0)
igef_start = 1
igefs, models, lines, datetimes = generators.generate_production(igef_start, date)
production_data = list(zip(igefs, models, lines, datetimes))

#print(production_data[:5])
#print('Anzahl Fahrzeuge:', len(production_data))

sql = """
    INSERT INTO models(model_id, model, drive_type)
    VALUES(%s, %s, %s)
"""
models_data = list(models_df.itertuples(index = False, name = None))
cursor.executemany(sql, models_data)
connection.commit()
'''
sql = 'SELECT * FROM models'
cursor.execute(sql)
res = cursor.fetchall()
print(res)

'''
sql = """INSERT INTO robot_types(robot_number, process_area) VALUES(%s, %s)"""

robot_types_data = list(robot_types_df.itertuples(index = False, name = None))
cursor.executemany(sql, robot_types_data)
connection.commit()

sql = """INSERT INTO robots(robot_id, robot_number, ubs_line) VALUES(%s, %s, %s)"""

robots_data = list(robots_df.itertuples(index = False, name = None))
cursor.executemany(sql, robots_data)
connection.commit()

sql = """INSERT INTO process_specifications(specification_id, model_id, robot_number, target_area_cm2, target_thickness_mm, target_volume_ml)
    VALUES(%s, %s, %s, %s, %s, %s)"""

specifications_data = list(specifications_df.itertuples(index = None, name = None))
cursor.executemany(sql, specifications_data)
connection.commit()

sql = """INSERT INTO production(igef, model_id, ubs_line, production_datetime)
VALUES (%s, %s, %s, %s)"""

cursor.executemany(sql, production_data)
connection.commit()


measurements_data = generators.generate_production_measurements(cursor)

sql = """INSERT INTO production_measurements(igef, specification_id, robot_id, actual_ml, deviation_percent, requires_inspection)
VALUES(%s, %s, %s, %s, %s, %s)
"""
cursor.executemany(sql, measurements_data)
connection.commit()
