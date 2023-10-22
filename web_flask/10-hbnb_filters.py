#!/usr/bin/python3
"""
A Flask web application to display states and their cities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City

app = Flask(__name__)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """
    Display a page with filters for States, Cities, and Amenities.
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    return render_template(
            '10-hbnb_filters.html', states=states, amenities=amenities)


@app.teardown_appcontext
def close_storage(exception):
    """
    Close the SQLAlchemy session after each request.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
