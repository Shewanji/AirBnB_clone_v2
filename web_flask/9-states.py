#!/usr/bin/python3
"""
A Flask web application to display states and their cities.
"""

from flask import Flask, render_template
from models import storage
from models.state import State
from models import *

app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """
    Close the SQLAlchemy session after each request.
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def state():
    """Displays a html page with states"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all')


@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """Display a list of states sorted by name or a specific state by ID."""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', states=state, mode='id')
    return render_template('9-states.html', states=state, mode='none')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
