from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='172.17.0.1:9092')

TIMEOUT = 20

results = [producer.send('test', b'hello').get(timeout=TIMEOUT) for i in range(10)]

print("done")