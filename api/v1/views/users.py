#!/usr/bin/python3
"""view for State objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """Creates an User"""
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in req_dict:
        return (jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in req_dict:
        return (jsonify({'error': 'Missing password'}), 400)
    new_user = User(**req_dict)
    storage.new(new_user)
    storage.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Retrieves the list of all State objects"""
    new_user = storage.get(User, user_id)
    if not new_user:
        abort(404)
    try:
        data = request.get_json()
    except:
        return {'error': 'Not a JSON'}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at',
                       'updated_at', 'email']:
            setattr(new_user, key, value)
    storage.save()
    return new_user.to_dict(), 200


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all City objects of a State"""
    return jsonify(list(
        map(lambda x: x.to_dict(),
            storage.all(User).values())
    ))


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return user.to_dict()


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(storage.get(User, user_id))
    storage.save()
    return {}, 200
