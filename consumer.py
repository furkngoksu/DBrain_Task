from kafka import KafkaConsumer
import json
import os
import time

# Helper function to wait for Kafka
def wait_for_kafka():
    retries = 10
    for i in range(retries):
        try:
            # Connect to Kafka
            consumer = KafkaConsumer(
                'test-topic',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='latest',
                group_id='my-consumer-group',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                api_version=(0, 10, 1)
            )
            print("Connected to Kafka")
            return consumer
        except Exception as e:
            print(f"Kafka not ready, retrying in 5 seconds... ({i+1}/{retries})")
            time.sleep(5)
    raise Exception("Could not connect to Kafka")

consumer = wait_for_kafka()

file_path = 'data.json'

# Load existing data from file
if os.path.exists(file_path):
    try:
        with open(file_path, 'r') as f:
            messages = json.load(f)
        print(f"Loaded existing data from {file_path}")
    except Exception as e:
        print(f"Failed to load existing data from {file_path}: {e}")
        messages = []
else:
    messages = []

# Helper function to check if data already exists
def data_exists(new_data, existing_data):
    return any(new_data == item for item in existing_data)

for message in consumer:
    received_data = message.value
    print(f"Received: {received_data}")

    if not data_exists(received_data, messages):
        messages.append(received_data)
        print(f"Added: {received_data}")

        try:
            with open(file_path, 'w') as f:
                json.dump(messages, f, indent=4)
            print(f"Data written to {file_path}")
        except Exception as e:
            print(f"Failed to write to {file_path}: {e}")
    else:
        print(f"Data already exists: {received_data}")
