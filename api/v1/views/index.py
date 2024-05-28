#!/usr/bin/python3
"""
index file
"""
import json
from flask import jsonify
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
    return json.dumps({"status": "OK"}, indent=4) + '\n'


@app_views.route('/stats', methods=['GET'])
def stats():
    """Return the count of all objects in each class"""
    classes = {
        'Amenity': Amenity,
        'BaseModel': BaseModel,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }
    counts = {}
    for cls_name, cls in classes.items():
        counts[cls_name] = storage.count(cls)
    return json.dumps(counts, indent=4) + '\n'
