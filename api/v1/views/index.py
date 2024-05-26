#!/usr/bin/python3
"""index file"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """return status"""
    return {"status": "OK"}


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    stats = {}
    for name, cls in classes.items():
        stats[name] = storage.count(cls)
    return stats
