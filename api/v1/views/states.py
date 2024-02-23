#!/usr/bin/python3
"""view for State objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    """Retrieves the list of all State objects"""
    return jsonify(list(map(lambda x: x.to_dict(),
                            storage.all(State).values())))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Retrieves the list of all State objects"""
    try:
        data = request.get_json()
    except:
        return {'error': 'Not a JSON'}, 400
    name = data.get('name')
    if not name:
        return {'error': 'Missing Name'}, 400
    new_state = State(name=name)
    storage.new(new_state)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Retrieves the list of all State objects"""
    new_state = storage.get(State, state_id)
    if not new_state:
        abort(404)
    try:
        data = request.get_json()
    except:
        return {'error': 'Not a JSON'}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(new_state, key, value)
    storage.save()
    return new_state.to_dict(), 201


@app_views.route('/states/<state_id>',  methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object"""
    if not storage.get(State, state_id):
        abort(404)
    return storage.get(State, state_id).to_dict()


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Retrieves a State object"""
    if not storage.get(State, state_id):
        abort(404)
    storage.delete(storage.get(State, state_id))
    storage.save()
    return {}, 200
