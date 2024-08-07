#!/usr/bin/python3
"""The first version of AirBnB clone Flask app"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


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


if __name__ == '__main__':
    host = ("0.0.0.0" if not getenv('HBNB_API_HOST')
            else getenv('HBNB_API_HOST'))
    port = 5000 if not getenv('HBNB_API_PORT') else getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
