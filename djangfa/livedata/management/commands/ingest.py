
import json
from kafka import KafkaConsumer, TopicPartition
from django.core.management.base import BaseCommand, CommandError

from ...models import RandomRun, RandomEntry


PARTITION_COUNT = 3

def decode(data):
    return json.loads(data.decode("utf-8"))


def save_to_db(msg):
    try:
        random_run = RandomRun.objects.get(run_id=msg.value['run_id'])
    except RandomRun.DoesNotExist:
        random_run = RandomRun(run_id=msg.value['run_id'])
        random_run.save(force_insert=True)
    random_entry = RandomEntry(
        random_run=random_run,
        payload=msg.value['number']
    )
    random_entry.save(force_insert=True)


def retrieve_previous_offsets(consumer, partitions):
    offsets = dict([(i, None) for i in range(len(partitions))])
    try:
        with open(".lockfile", 'r') as lockfile:
            restored_offsets = json.loads(lockfile.readline())
            for partition, offset in restored_offsets.items():
                print(f"Resuming consumer for partition {partition} at position {offset}")
                if offset:
                    consumer.seek(partitions[int(partition)], offset + 1)
    except FileNotFoundError as e:
        print("starting a new consumer from the latest position")
    return offsets


def update_offsets(msg, offsets):
    offsets[msg.partition] = msg.offset
    with open(".lockfile", 'w') as lockfile:
        lockfile.seek(0)
        lockfile.write(json.dumps(offsets))


class Command(BaseCommand):
    help = 'Pulls in data from kafka'

    def handle(self, *args, **options):
        consumer = KafkaConsumer(bootstrap_servers='172.17.0.1:9092', value_deserializer=decode)
        partitions = [TopicPartition(topic='test', partition=i) for i in range(PARTITION_COUNT)]
        consumer.assign(partitions)

        offsets = retrieve_previous_offsets(consumer, partitions)

        for msg in consumer:
            print(f"{msg.partition} - {msg.offset} - {msg.value}")
            save_to_db(msg)
            update_offsets(msg, offsets)

        self.stdout.write(self.style.SUCCESS('Finished'))
