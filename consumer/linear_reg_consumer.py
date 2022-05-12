from server.mongo import client
from model.linear_reg_predict import LinearRegServing

from time import sleep
from json import loads
from kafka import KafkaConsumer


TOPIC_NAME = 'housing-prediction-events'

linear_reg_srv = LinearRegServing('./model/linearReg.model')

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    value_deserializer=lambda x: loads(x.decode('utf-8')))


for message in consumer:
    task = message.value
    print('Received task: {}'.format(task['task_id']))
    print('Start predicting...')
    batch_input = task['input_list']
    ret = linear_reg_srv.predict_batch(batch_input)
    
    print('Prediction finished.')
    print(ret)
    

    
    