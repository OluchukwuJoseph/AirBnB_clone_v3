#!/usr/bin/python3
""" The first version of AirBnB clone Flask app """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """This method is triggered when users query a non-existing URI"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    """This method removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == "__main__":
    if os.getenv('HBNB_API_HOST'):
        host = os.getenv('HBNB_API_HOST')
    else:
        host = "0.0.0.0"

    if os.getenv('HBNB_API_PORT'):
        port = os.getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host, port, threaded=True, debug=True)
