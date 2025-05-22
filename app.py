from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from models.auth import User
from db import get_db
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key' # replace with a secure key

# Register blueprints
from routes.employees import employees
app.register_blueprint(employees, url_prefix='/employees')

from routes.auth import auth
app.register_blueprint(auth)


# Initialise Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'

# Base routes
@app.route('/')
def index():
    return redirect(url_for('auth.dashboard'))

@login_manager.user_loader
def load_user(user_id):
    """Load user from the database using user_id."""
    db = get_db()
    user = db.execute("SELECT * FROM Users WHERE pk_user_id = ?", (user_id,)).fetchone()
    if user:
        return User(user['pk_user_id'], user['fk_employee_id'], user['username'], user['password'], user['forgot_password'], user['admin'])
    return None



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

if __name__ == '__main__':
    app.run(debug=True)