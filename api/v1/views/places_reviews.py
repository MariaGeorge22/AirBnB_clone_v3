#!/usr/bin/python3
"""view for Place objects"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    new_place = storage.get(Place, place_id)
    if not new_place:
        abort(404)
    data = request.get_json()
    if not data:
        return {'error': 'Not a JSON'}, 400
    user_id = data.get('user_id')
    if not user_id:
        return {'error': 'Missing user_id'}, 400
    if not storage.get(User, user_id):
        abort(404)
    text = data.get('text')
    if not text:
        return {'error': 'Missing text'}, 400
    data['place_id'] = place_id
    new_review = Review(**data)
    storage.new(new_review)
    storage.save()
    return new_review.to_dict(), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Retrieves the list of all Place objects"""
    new_review = storage.get(Review, review_id)
    if not new_review:
        abort(404)
    data = request.get_json()
    if not data:
        return {'error': 'Not a JSON'}, 400
    for key, value in data.items():
        if key not in ['id', 'created_at',
                       'updated_at', 'place_id', 'user_id']:
            setattr(new_review, key, value)
    storage.save()
    return new_review.to_dict(), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(list(map(lambda x: x.to_dict(), place.reviews)))


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return review.to_dict()


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    if not storage.get(Review, review_id):
        abort(404)
    storage.delete(storage.get(Review, review_id))
    storage.save()
    return {}, 200
