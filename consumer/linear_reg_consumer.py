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

def handle_task(task_id):
    print('Received task: {}'.format(task_id))
    print('Start predicting...')
    
    task_record = coll_task.find_one({'task_id' : task_id})
    batch_input = task_record['input_list']

    #update status to predicting
    coll_task.update_one({'task_id' : task_id}, {
        "$set": {
            'status': task_status.TASK_PREDICTING,
        }
    })

    # batch_input = task['input_list']
    df_ret = linear_reg_srv.predict_batch(batch_input)
    
    predictions = df_ret['prediction'].values.tolist()
    
    print('Prediction finished.')
    
    # update task record in mongo

    coll_task.update_one({'task_id' : task_id}, { 
        "$set": {
            'status': task_status.TASK_SUCCEED,
            'predictions': predictions,
        }
    })
    print('Batch prediction succeeds.')

for message in consumer:
    task = message.value
    task_id = task['task_id']
    try:
        handle_task(task_id)
    except Exception as e:
        print(e)
        coll_task.update_one({'task_id' : task_id}, {
        "$set": {
            'status': task_status.TASK_ABORT,
        }
    })
    
    
    