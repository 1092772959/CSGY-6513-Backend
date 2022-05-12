
from time import sleep
from json import dumps
from uuid import uuid1
from kafka import KafkaProducer

TOPIC_NAME = 'housing-prediction-events'

features_one = [0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98]
features_two = [0.02731,0,7.07,0,0.469,6.421,78.9,4.9671,2,242,17.8,396.9,9.14]

'''
Data Format: 

    features = [0.00632,18,2.31,0,0.538,6.575,65.2,4.09,1,296,15.3,396.9,4.98]

    data = {
        'task_id': 1000,
        'features': [
            [...],
            [...],
        ],
    }

'''

data = {
    'task_id': str(uuid1().int >> 64),
    'input_list': [
        features_one,
        features_two,
     ],
}

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8'))

producer.send(TOPIC_NAME, value=data)
sleep(1)
