import json

from kafka import KafkaConsumer, TopicPartition

PARTITION_COUNT = 3

def decode(data):
    return json.loads(data.decode("utf-8"))

consumer = KafkaConsumer(bootstrap_servers='172.17.0.1:9092', value_deserializer=decode)
partitions = [TopicPartition(topic='test', partition=i) for i in range(PARTITION_COUNT)]
consumer.assign(partitions)

offsets = dict([(i, None) for i in range(PARTITION_COUNT)])
try:
    with open(".lockfile", 'r') as lockfile:
        restored_offsets = json.loads(lockfile.readline())
        for partition, offset in restored_offsets.items():
            print(f"Resuming consumer for partition {partition} at position {offset}")
            if offset:
                consumer.seek(partitions[int(partition)], offset + 1)
except FileNotFoundError as e:
    print("starting a new consumer from the latest position")

for msg in consumer:
    print(f"{msg.offset} - {msg.value}")
    offsets[msg.partition] = msg.offset
    with open(".lockfile", 'w') as lockfile:
        lockfile.seek(0)
        lockfile.write(json.dumps(offsets))