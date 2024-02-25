#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Representation of city """
    if models.storage_t == "db":
        __tablename__ = 'cities'
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        name = Column(String(128), nullable=False)
        places = relationship("Place", backref="cities")
    else:
        state_id = ""
        name = ""

        @property
        def places(self):
            """getter attribute returns the list of Place instances"""
            place_list = []
            from models.place import Place
            from models import storage
            all_places = storage.all(Place)
            for place in all_places.values():
                if place.city_id == self.id:
                    place_list.append(place)
            return place_list

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
