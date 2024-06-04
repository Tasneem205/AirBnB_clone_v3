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
    response = jsonify(state.to_dict())
    return response, 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a state"""
    state = storage.get(Amenity, amenity_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    response = jsonify({})
    return response, 200


@app_views.route('/amenities/', methods=['POST'])
def add_new_amenity():
    """create a new instance of state"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        abort(400)
    if 'name' not in request.get_json():
        abort(400)
    js = request.get_json()
    obj = Amenity(**js)
    obj.save()
    response = jsonify(obj.to_dict())
    return response, 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ put method """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        abort(400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    data = jsonify(obj.to_dict())
    return data, 200
