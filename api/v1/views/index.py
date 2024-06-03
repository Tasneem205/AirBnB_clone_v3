#!/usr/bin/python3
"""
index file
"""
import json
from flask import jsonify, Response
from . import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """Returns a JSON status"""
    res = {"status": "OK"}
    response = Response(res, mimetype='application/json')
    return jsonify(res)


@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the count of all objects in each class"""
    classes = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    counts = {}
    for cls_name, cls in classes.items():
        counts[cls_name] = storage.count(cls)
    return jsonify(counts)
