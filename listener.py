from kafka import KafkaConsumer

consumer = KafkaConsumer('test', bootstrap_servers='172.17.0.1:9092')

for msg in consumer:
    print (msg)