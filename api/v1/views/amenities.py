#!/usr/bin/python3
"""
states view
"""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views
import json


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenities objects"""
    states = storage.all(Amenity).values()
    states_list = [state.to_dict() for state in states]
    response = json.dumps(states_list, indent=4) + '\n'
    return response


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a State object"""
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    response = json.dumps(state.to_dict(), indent=4) + '\n'
    return response


@app_views.route('/amenities/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(state_id):
    """delete a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    response = json.dumps({}, indent=4) + '\n'
    return response


@app_views.route('/amenities/', methods=['POST'])
def add_new_amenity():
    """create a new instance of state"""
    if not request.get_json():
        response = json.dumps({"error": "Not a JSON"}, indent=4) + '\n'
        return response, 400
    if 'name' not in request.get_json():
        response = json.dumps({"error": "Missing name"}, indent=4) + '\n'
        return response, 400
    js = request.get_json()
    obj = State(**js)
    obj.save()
    response = json.dumps(obj.to_deict, indent=4) + '\n'
    return response, 201


@app_views.route('/amenities/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(state_id):
    """ put method """
    if not request.get_json():
        response = json.dumps({"error": "Not a JSON"}, indent=4) + '\n'
        return response, 400
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    response = json.dumps(obj.to_dict(), indent=4) + '\n'
    return response
