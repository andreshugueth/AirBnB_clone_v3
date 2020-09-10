#!/usr/bin/python3
"""New Funtion places"""
from api.v1.views import app_views
from models.city import City
from models.state import State
from models.place import Place
from models import storage
from flask import jsonify, abort, request, make_response


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_all_cities(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    list_dict = []
    for obj in city.places:
        list_dict.append(obj.to_dict())
    return make_response(jsonify(list_dict), 200)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(place_id):
    """Retrieves a Place object"""
    obj = storage.get(Place, place_id)
    if (obj):
        return make_response(jsonify(obj.to_dict()), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """Deletes a Place object"""
    obj = storage.get(Place, place_id)
    if (obj):
        storage.delete(obj)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place_create(city_id):
    """Creates a User"""
    cities = storage.get('City', city_id)
    if not cities:
        abort(404)
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    if 'user_id' not in place.keys():
        abort(400, {'Missing user_id'})
    userid = storage.get('User', place['user_id'])
    if not userid:
        abort(404)
    if 'name' not in place:
        abort(400, {'Missing name'})
    new_place = Place(**place)
    new_place.city_id = city_id
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)



@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a User object"""
    place = request.get_json()
    if not place:
        abort(400, {'Not a JSON'})
    places = storage.get('Place', place_id)
    if not places:
        abort(404)

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in place.items():
        if key not in ignore:
            setattr(places, key, value)
    storage.save()
    return make_response(jsonify(places.to_dict()), 200)
