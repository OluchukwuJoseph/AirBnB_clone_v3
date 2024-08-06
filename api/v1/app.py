#!/usr/bin/python3
"""The first version of AirBnB clone Flask app"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """This method removes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """This method is triggered when users query a non-existing URI"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = ("0.0.0.0" if not getenv('HBNB_API_HOST')
            else getenv('HBNB_API_HOST'))
    port = 5000 if not getenv('HBNB_API_PORT') else getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
