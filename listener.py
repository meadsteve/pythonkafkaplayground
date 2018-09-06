import json

from kafka import KafkaConsumer, TopicPartition


def decode(data):
    return json.loads(data.decode("utf-8"))

consumer = KafkaConsumer(bootstrap_servers='172.17.0.1:9092', value_deserializer=decode)
partition = TopicPartition(topic='test', partition=0)
consumer.assign([partition])

try:
    with open(".lockfile", 'r') as lockfile:
        last_position = int(lockfile.readline())
        print(f"resuming consumer at position {last_position}")
        consumer.seek(partition, last_position + 1)
except:
    print("starting a new consumer from the latest position")

for msg in consumer:
    print(f"{msg.offset} - {msg.value}")
    with open(".lockfile", 'w') as lockfile:
        lockfile.seek(0)
        lockfile.write(str(msg.offset))