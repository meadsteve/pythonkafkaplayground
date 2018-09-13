import json
import uuid

from kafka import KafkaProducer


class SimplePublisher:
    TIMEOUT = 20

    def __init__(self, topic):
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers='172.17.0.1:9092', partitioner=self._partition)

    def push(self, data, key):
        return self.producer\
            .send(self.topic, self._encode(data), key=bytearray(f"{key}", "utf-8"))\
            .get(timeout=self.TIMEOUT)

    def _partition(self, key, partitions, *args):
        return int(key) % len(partitions)

    def _encode(self, data):
        return bytearray(json.dumps(data), "utf-8")


publisher = SimplePublisher(topic="test")

RUN_ID = str(uuid.uuid4())

for j in range(20):
    requests = [publisher.push(data={"number": f"{j}-{i}", "run_id": RUN_ID}, key=i) for i in range(10)]

print("done")