#!/usr/bin/python3
"""view for State objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an Amenity"""
    data = request.get_json()
    if not data:
        return {'error': 'Not a JSON'}, 400
    name = data.get('name')
    if not name:
        return {'error': 'Missing Name'}, 400
    new_amenity = Amenity(name=name)
    storage.new(new_amenity)
    storage.save()
    return new_amenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Retrieves the list of all State objects"""
    new_amenity = storage.get(Amenity, amenity_id)
    if not new_amenity:
        abort(404)
    data = request.get_json()
    if not data:
        return {'error': 'Not a JSON'}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at',
                       'updated_at']:
            setattr(new_amenity, key, value)
    storage.save()
    return new_amenity.to_dict(), 200


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all City objects of a State"""
    return jsonify(list(map(lambda x: x.to_dict(),
                            storage.all(Amenity).values())))


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return amenity.to_dict()


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(storage.get(Amenity, amenity_id))
    storage.save()
    return {}, 200
