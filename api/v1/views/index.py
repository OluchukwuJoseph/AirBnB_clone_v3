#!/usr/bin/python3
"""Index Module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns API status"""
    data = {"status": "OK"}
    return jsonify(data)
