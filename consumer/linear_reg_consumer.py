from mongo import coll_task
from model.linear_reg_predict import LinearRegServing
from config import task_status

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
    task_id = task['task_id']
    print('Received task: {}'.format(task_id))
    print('Start predicting...')
    batch_input = task['input_list']
    df_ret = linear_reg_srv.predict_batch(batch_input)
    
    predictions = df_ret['prediction'].values.tolist()
    
    print('Prediction finished.')
    
    # update task record in mongo
    task_record = coll_task.find_one({'task_id' : task_id})
    task_record['status'] = task_status.TASK_SUCCEED
    task_record['predictions'] = predictions

    coll_task.update_one({'task_id' : task_id}, { 
        "$set": {
            'status': task_status.TASK_SUCCEED,
            'predictions': predictions,
        }
    })
    print('Update task finished.')

    
    