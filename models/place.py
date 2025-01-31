#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
import models
from models.review import Review
from os import getenv
from models.amenity import Amenity


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    if getenv('HBNB_TYPE_STORAGE') == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(128), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
                "Review", backref="place", cascade="all, delete-orphan")
        amenities = relationship(
            "Amenity", secondary=place_amenity, viewonly=False,
            backref="place_amenities")
        amenity_ids = []
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

    @property
    def reviews(self):
        """Get a list of all linked Reviews."""
        rev_list = []
        for rev in models.storage.all(Review).values():
            if rev.place_id == self.id:
                rev_list.append(rev)
        return rev_list

    @property
    def amenities(self):
        """returns the list of Amenity instances"""
        amn_list = []
        for amn in models.storage.all(Amenity).values():
            if amn.id in self.amenity_ids:
                amn_list.append(amn)
        return amn_list

    @amenities.setter
    def amenities(self, value):
        """handles append method for adding an Amenity.id
        to the attribute amenity_ids"""
        if isinstance(value, Amenity):
            self.amenity_ids.append(value.id)

    def __repr__(self):
        """return a string representation of the object"""
        return "[Place] ({}) {}".format(self.id, self.to_dict())
