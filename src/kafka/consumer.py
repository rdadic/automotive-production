import json 
import os 
from pathlib import Path 
from dotenv import load_dotenv
from kafka import KafkaConsumer

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

TOPIC = "productionUBS"

def main():
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    consumer = KafkaConsumer(
        TOPIC, 
        bootstrap_servers = bootstrap_servers,
        group_id = "production_ubs_consumer",
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer = lambda value: json.loads(value.decode("utf-8")),
        
    )

    print(f"Listening to topic: {TOPIC}")

    try:
        for message in consumer:
            event = message.value

            print(
                f"IGEF: {event['igef']} -- "
                f"{event['model']} -- "
                f"{event['drive_type']} -- "
                f"UBS Linie: {event['ubs_line']} -- "
                f"at {event['production_datetime']}"
            )

    except KeyboardInterrupt:
        print('Cosumer stopped')

    finally:
        consumer.close()
 
if __name__ == "__main__":
    main()


