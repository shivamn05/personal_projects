import sqlite3

from flask import Flask, g, redirect, render_template, session
from functools import wraps
from datetime import time

app = Flask(__name__)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

# Source: ChatGPT
DATABASE = 'system.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # allows you to access rows like dictionaries
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Source: ChatGPT
# For timeslot selection
hour = 13
t = time(hour=hour)
formatted = t.strftime("%I:00 %p")
print(formatted)