from flask_login import UserMixin

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import InputRequired, Length

from db import get_db

# Create a user object for flask-login library
class User(UserMixin):
    def __init__(self, id, employee_id, username, password, forgot_password, admin):
        self.id = id
        self.employee_id = employee_id
        self.username = username
        self.password = password
        self.forgot_password = forgot_password
        self.admin = admin

    @staticmethod
    def get(username):
        user_data = getUserData(username)

        if user_data:
            return User(
                user_data['pk_user_id'],
                user_data['fk_employee_id'],
                user_data['username'],
                user_data['password'],
                user_data['forgot_password'],
                user_data['admin']
            )
        return None

# Create forms to be used on login page
class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username:', validators=[InputRequired(), Length(min=3)])
    password = PasswordField('Password:', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """Form for user registration."""
    employee_id = IntegerField('Employee ID:', validators=[InputRequired()])
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Register')




# Helper Functions

def getUserData(username):
    """
    Helper function to get all user data based on username.
    """
    db = get_db()
    query = """
        SELECT * FROM Users
        WHERE username = ?
    """
    values = (username,)

    return db.execute(query, values).fetchone()

def isEmployeeIdRegistered(id):
    """
    Helper function to check if an employee ID has already been registered.
    """
    db = get_db()
    query = """
        SELECT username FROM Users
        WHERE fk_employee_id = ?
    """
    values = (id,)
    user = db.execute(query, values).fetchone()
    if user:
        return True
    return False

def usernameTaken(username):
    """
    Helper function to check if a username has been taken already 
    """
    db = get_db()
    query = """
        SELECT username, pk_user_id FROM Users
        WHERE username = ?
    """
    values = (username,)
    user = db.execute(query, values).fetchone()
    print(user)
    if user:
        return True
    return False



# Models for routes

def registerUser(data):
    """
    Creates a record in the Users table for a new account.
    Args:
        data (dict): Account data in the format:
            'employee_id'
            'username'
            'hashed_password'
    """
    try:
        # Get account details
        employee_id = data['employee_id']
        username = data['username']
        hashed_password = data['hashed_password']

        # Create query
        query = """
            INSERT INTO Users (fk_employee_id, username, password) 
            VALUES (?, ?, ?)
        """
        values = (employee_id, username, hashed_password)

        db = get_db()
        db.execute(query, values)
        db.commit()

        return 'success'
    except Exception as e:
        raise e

def upgradeUser(id):
    """
    Upgrades a user ID to an admin account. The route should be protected by an admin-only login.
    Args:
        id (int): The User ID to upgrade
    """
    try:
        query = """
            UPDATE Users
            SET admin = 1
            WHERE pk_user_id = ?
        """
        values = (id,)

        db = get_db()
        db.execute(query, values)
        db.commit()

        return 'success'
    except Exception as e:
        raise e

def forgotPassword(id):
    """
    Sets the forgot_password attribute for the specified account to 1 (true).
    Args:
        id (int): The User ID (not to be confused with employee ID)
    """
    try:
        query = """
            UPDATE Users 
            SET forgot_password = 1 
            WHERE pk_user_id = ?
        """
        values = (id,)

        db = get_db()
        db.execute(query, values)
        db.commit()

        return 'success'
    except Exception as e:
        raise e