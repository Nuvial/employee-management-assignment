from flask import Flask, render_template
from db import get_db
import sqlite3

from routes.employees import employees

app = Flask(__name__)
app.register_blueprint(employees, url_prefix='/employees')


# Database initialisation code
def init_db():
    """Function to initialise the sqlite database"""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def inidb_command():
    """Call to initialise the database."""
    init_db()
    print("Database initialised.")
