#!/usr/bin/python3
"""Flask App"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """This method removes the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    host = ("0.0.0.0" if not getenv('HBNB_API_HOST')
            else getenv('HBNB_API_HOST'))
    port = 5000 if not getenv('HBNB_API_PORT') else getenv('HBNB_API_PORT')

    app.run(host=host, port=port, threaded=True)
