#!/usr/bin/python3
"""
states view
"""
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    states_list = [state.to_dict() for state in states]
    response = jsonify(states_list)
    return response


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    response = jsonify(state.to_dict())
    return response


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    response = jsonify({})
    return response


@app_views.route('/states/', methods=['POST'])
def add_new_state():
    """create a new instance of state"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        response = jsonify({"error": "Missing name"})
        return response, 400
    js = request.get_json()
    obj = State(**js)
    obj.save()
    response = jsonify(obj.to_dict())
    return response, 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_method(state_id):
    """ put method """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    response = jsonify(obj.to_dict())
    return response
