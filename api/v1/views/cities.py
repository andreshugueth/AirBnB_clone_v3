#!/usr/bin/python3
"""New Funtion states"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models.city import City
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_all_city(state_id):
    """All cities"""
    states_id = storage.get('State', state_id)
    if state_id is None:
        abort(404)
    list_dict = []
    for obj in storage.all(City).values():
        if obj.state_id == state_id:
            list_dict.append(obj.to_dict())
    return jsonify(list_dict), 200


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    """Retrieves city object"""
    city = storage.get("City", city_id)
    if (city):
        return jsonify(city.to_dict()), 200
    else:
        abort(404)


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """delete method api"""
    city = storage.get("City", city_id)
    if (city):
        storage.delete(city)
        storage.save()
        return jsonify(({}), 200)
    else:
        abort(404)


@app_views.route('/states/<string:state_id>/cities', methods=['POST'], strict_slashes=False)
def post_city_create(state_id):
    """comet"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    conten = request.get_json()
    if conten is None:
        return jsonify(({"error": "Not a JSON"}), 400)
    elif conten.get('name') is None:
        return jsonify(({"error": "Missing name"}), 400)

    conten['state_id'] = state_id
    new_city = City(**conten)
    storage.new(new_city)
    storage.save()
    return jsonify((new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(city_id):
    """update a instance of City"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, attr, val)
    storage.save()
    return jsonify((city.to_dict()), 200)
