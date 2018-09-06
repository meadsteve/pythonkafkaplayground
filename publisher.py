import json
import uuid

from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='172.17.0.1:9092')

TIMEOUT = 20
RUN_ID = str(uuid.uuid4())


def encode(data):
    return bytearray(json.dumps(data), "utf-8")

for j in range(20):
    requests = [producer.send('test', encode({"number": f"{j}-{i}", "run_id": RUN_ID})) for i in range(10)]
    results = [request.get(timeout=TIMEOUT) for request in requests]

print("done")