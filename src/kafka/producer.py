import json 
import os 
from pathlib import Path 
import mysql.connector as connector
from dotenv import load_dotenv
from kafka import KafkaProducer

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

TOPIC = "productionUBS"

def get_production_rows():
    connection = connector.connect(
        host = os.environ["MYSQL_HOST"],
        port = int(os.getenv("MYSQL_PORT","3306")),
        database = os.environ["MYSQL_DATABASE"],
        user = os.environ["MYSQL_USER"],
        password = os.environ["MYSQL_PASSWORD"],
    )

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT production.igef, models.model, models.drive_type, production.ubs_line, production.production_datetime FROM production
            INNER JOIN models ON production.model_id = models.model_id ORDER BY production_datetime, igef
        """)
        rows = cursor.fetchall()
        cursor.close()
        return rows 
    
    finally:
        connection.close()
    
def json_serializer(value):
    return json.dumps(value, default = str).encode("utf-8")

def main():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    rows = get_production_rows()

    print(f"Found {len(rows)} existing production records - cars")

    producer = KafkaProducer(
        bootstrap_servers = bootstrap_servers,
        key_serializer = lambda key: str(key).encode("utf-8"),
        value_serializer=json_serializer,
        acks="all",
    )

    try:
        for row in rows:
            event = {
                "igef": row["igef"],
                "model": row["model"],
                "drive_type": row["drive_type"],
                "ubs_line": row["ubs_line"],
                "production_datetime": row["production_datetime"],
            }

            producer.send(
                TOPIC,
                key = row["igef"],
                value = event
            ).get(timeout=30)

            print(
                f"IGEF: {row['igef']} - {row['model']} - {row['drive_type']} on UBS line {row['ubs_line']} at {row['production_datetime']}"
            )

    finally:
        producer.flush()
        producer.close()

if __name__ == "__main__":
    main()