from flask import Flask
from flask import request
from flask_cors import CORS
import csv
import io
from uuid import uuid1

from mongo import coll_housing, coll_task
from model.linear_reg_predict import LinearRegServing
from producer.prediction_producer import send_batch

def create_app(test_config=None):
    app = Flask(__name__)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app)

    ATTR_LABELS = ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat']

    linear_reg_srv = LinearRegServing('./model/linearReg.model')

    def resp_missing_feat():
        resp = {
            "code" : -1,
            "message": "missing features",
        }
        return resp

    @app.route("/predict/linear", methods=["POST"])
    def linear_predict():
        form = request.form
        feat = []
        for attr in ATTR_LABELS:
            if attr not in form.keys():
                resp = resp_missing_feat()
                return resp
            feat.append(float(form.get(attr)))
        
        print(feat)
        ret = linear_reg_srv.predict(feat)
        resp = {
            "code": 0,
            "message": "succeed",
            "data": ret,
        }
        print(resp)
        return resp

    @app.route("/predict/linear/batch", methods=["POST"])
    def linear_predict_batch():
        f = request.files['input_file']
        stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
        reader = csv.reader(stream)
        data = []
        for row in reader:
            n_row = []
            for item in row:
                n_row.append(float(item))
            data.append(n_row)
        
        send_batch(data)
        
        return {
            "code": 0,
            "data": data,
        }

    @app.route("/predict/linear/batch/<task_id>", methods=["GET"])
    def get_batch_result(task_id):
        task = coll_task.find_one({'task_id': task_id})
        rets = []
        input_list = task['input_list']
        predict_list = task['predictions']
        
        assert(len(input_list) == len(predict_list))

        for i in range(0, len(input_list)):
            input_feat = input_list[i]
            
            ret_dict = {ATTR_LABELS[i]: input_feat[i] for i in range(len(input_feat))}
            ret_dict['prediction'] = predict_list[i]
            rets.append(ret_dict)

        return {
            "code": 0,
            "data": rets,
        }

    @app.route("/predict/linear/tasks", methods=["GET"])
    def get_tassk_ids():
        cursor = coll_task.find({}, {'task_id': 1, 'status': 1, '_id' : 0})
        rets = []
        for item in cursor:
            rets.append(item)
        print(rets)

        return {
            "code" : 0,
            "data": rets,
        }
        

    @app.route("/housing/<id>", methods=["GET"])
    def get_housing_by_id(id):
        print(id)
        data = coll_housing.find_one({"" : int(id)}, {"_id" : 0})
        print(data)
        
        resp = {
            "code": 0,
            "data": data,
        }
        return resp

    @app.route("/predict", methods=["POST"])
    def predict():
        form = request.form
        
        return {
            "result" : 10.0,
        }

    @app.route("/data/price", methods=["GET"])
    def get_price():
        data = [
            24.00,
            21.60,
            34.70
        ]
        resp = {
            "data": data,
        }
        return resp

    return app
