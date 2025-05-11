from flask import request, jsonify, Blueprint, render_template, redirect, request, url_for, flash
from flask_login import UserMixin, login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from flask_bcrypt import Bcrypt
import sqlite3

from db import get_db

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, id, employee_id, username, password, admin):
        self.id = id
        self.employee_id = employee_id
        self.username = username
        self.password = password
        self.admin = admin
    
    @staticmethod
    def get(username):
        db = get_db()
        user_data = db.execute("SELECT * FROM Users WHERE username = ?", (username,)).fetchone()
        db.close()
        if user_data:
            return User(
                user_data['pk_user_id'],
                user_data['fk_employee_id'],
                user_data['username'],
                user_data['password'],
                user_data['admin']
            )
        return None


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.get(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('auth.dashboard'))
        flash('Invalid Credentials', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db = get_db()
        try:
            db.execute("INSERT INTO Users (username, password, fk_employee_id, admin) VALUES (?, ?, 6, 1)", (username, hashed_password))
            db.commit()
            flash('Registration Successful! You may now log in.', 'success')
            return redirect(url_for('auth.login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')
        finally:
            db.close()
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
