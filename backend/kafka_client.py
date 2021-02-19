from pykafka import KafkaClient

def get_kafka_client():
    return KafkaClient('kafka:9092')