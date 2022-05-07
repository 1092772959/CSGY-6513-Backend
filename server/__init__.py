from flask import Flask
from flask import make_response


def create_app(test_config=None):
    app = Flask(__name__)

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
