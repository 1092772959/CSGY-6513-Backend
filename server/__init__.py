from flask import Flask
from flask import request

from server.mongo import Coll_housing
from server.linear_reg_predict import LinearRegServing

def create_app(test_config=None):
    app = Flask(__name__)

    ATTR_LABELS = ['crim', 'zn', 'indus', 'chas', 'nox', 'rm', 'age', 'dis', 'rad', 'tax', 'ptratio', 'b', 'lstat']

    linear_reg_srv = LinearRegServing('./server/model/linearReg.model')

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
        
        # print(feat)
        ret = linear_reg_srv.predict(feat)
        resp = {
            "code": 0,
            "message": "succeed",
            "data": ret,
        }
        return resp

    @app.route("/housing/<id>", methods=["GET"])
    def get_housing_by_id(id):
        print(id)
        data = Coll_housing.find_one({"" : int(id)}, {"_id" : 0})
        print(data)
        
        resp = {
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


    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    return app
