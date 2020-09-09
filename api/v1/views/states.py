#!/usr/bin/python3
"""State objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, abort, request, make_response
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def list_state():
    """Retrieves the list of all State objects"""
    state_list = []
    for state in storage.all("State").values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def state_obj(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    state.delete
    storage.save
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    response = request.get_json
    if response is None:
        return make_response("Not a JSON", 400)
    if 'name' not in response:
        return make_response("Missing name", 400)
    state = State(**response)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a states"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state, attr, val)
    storage.save()
    return jsonify(state.to_dict())
