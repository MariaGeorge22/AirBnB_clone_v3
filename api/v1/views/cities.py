#!/usr/bin/python3
"""view for State objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    new_state = storage.get(State, state_id)
    if not new_state:
        abort(404)
    try:
        data = request.get_json()
    except:
        return {'error': 'Not a JSON'}, 400
    name = data.get('name')
    if not name:
        return {'error': 'Missing Name'}, 400
    new_city = City(name=name, state_id=state_id)
    storage.new(new_city)
    storage.save()
    return new_city.to_dict(), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Retrieves the list of all State objects"""
    new_city = storage.get(City, city_id)
    if not new_city:
        abort(404)
    try:
        data = request.get_json()
    except:
        return {'error': 'Not a JSON'}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at',
                       'updated_at', 'state_id']:
            setattr(new_city, key, value)
    storage.save()
    return new_city.to_dict(), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(list(map(lambda x: x.to_dict(), state.cities)))


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return city.to_dict()


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    if not storage.get(City, city_id):
        abort(404)
    storage.delete(storage.get(City, city_id))
    storage.save()
    return {}, 200
