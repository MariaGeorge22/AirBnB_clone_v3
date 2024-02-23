#!/usr/bin/python3
"""view for City objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    new_city = storage.get(City, city_id)
    if not new_city:
        abort(404)
    data = request.get_json()
    if not data:
        return {'error': 'Not a JSON'}, 400
    user_id = data.get('user_id')
    if not user_id:
        return {'error': 'Missing user_id'}, 400
    if not storage.get(User, user_id):
        abort(404)
    name = data.get('name')
    if not name:
        return {'error': 'Missing name'}, 400
    data['city_id'] = city_id
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return new_place.to_dict(), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Retrieves the list of all City objects"""
    new_place = storage.get(Place, place_id)
    if not new_place:
        abort(404)
    data = request.get_json()
    if not data:
        return {'error': 'Not a JSON'}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at',
                       'updated_at', 'city_id', 'user_id']:
            setattr(new_place, key, value)
    storage.save()
    return new_place.to_dict(), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(list(map(lambda x: x.to_dict(), city.places)))


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return place.to_dict()


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    if not storage.get(Place, place_id):
        abort(404)
    storage.delete(storage.get(Place, place_id))
    storage.save()
    return {}, 200
