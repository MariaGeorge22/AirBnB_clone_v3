#!/usr/bin/python3
"""view for Place objects"""

import os
from flask import abort, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """Creates a Amenity"""
    new_place = storage.get(Place, place_id)
    if not new_place:
        abort(404)
    new_amenity = storage.get(Amenity, amenity_id)
    if not new_amenity:
        abort(404)
    if new_amenity in new_place.amenities:
        return new_amenity.to_dict(), 200
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        new_place.amenity_ids = list(map(lambda x: x.id, new_place.amenities))
        new_place.amenity_ids.append(new_amenity.id)
        new_place.save()
    else:
        new_place.amenities.append(new_amenity)
        storage.save()
    return new_amenity.to_dict(), 201


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(list(map(lambda x: x.to_dict(), place.amenities)))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    place = storage.get(Place, place_id)
    if not (amenity and
            place and
            amenity in place.amenities):
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        place.amenity_ids = list(map(lambda y: y.id,
                                     filter(lambda x: x.id != amenity_id,
                                            place.amenities)))
        place.save()
    else:
        storage.delete(amenity)
        storage.save()
    return {}, 200
