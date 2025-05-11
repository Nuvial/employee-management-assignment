from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username:', validators=[InputRequired(), Length(min=3)])
    password = PasswordField('Password:', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username:', validators=[InputRequired(), Length(min=3, max=25)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Register')