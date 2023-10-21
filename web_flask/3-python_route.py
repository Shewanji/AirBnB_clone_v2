#!/usr/bin/python3
"""
A Flask web application with three routes:
- /: Displays "Hello HBNB!"
- /hbnb: Displays "HBNB"
- /c/<text>: Displays "C " followed by the value of the text variable,
replacing underscores with spaces.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display "Hello HBNB!" on the root route."""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display "HBNB" on the /hbnb route."""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """
    Display "C " followed by the value of the text variable
    (replace underscores with spaces).

    :param text: The text to be displayed, with underscores replaced by spaces.
    :type text: str
    """
    text_with_spaces = text.replace("_", " ")
    return f'C {text_with_spaces}'


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """
    Display "Python " followed by the value of the text variable
    (replace underscores with spaces).

    :param text: The text to be displayed, with underscores replaced by spaces.
    :type text: str
    """
    text_with_spaces = text.replace("_", " ")
    return f'Python {text_with_spaces}'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
