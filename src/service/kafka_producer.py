from src.config.kafka import producer

TOPIC = "image-analysis-result"

def publish_analysis(result):

    producer.send(TOPIC, result)

    producer.flush()