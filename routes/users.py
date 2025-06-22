from flask import request, jsonify, Blueprint, render_template
from flask_login import login_required, current_user
from flask_bcrypt import Bcrypt

from .models.users import getUsers, deleteUser, changePassword, changeUsername
from .models.auth import isEmployeeIdRegistered, usernameTaken, registerUser, upgradeUser, demoteUser
from .auth import admin_required

users = Blueprint('users', __name__)
bcrypt = Bcrypt()

@users.route('/')
@login_required
def index():
    return render_template('users.html', active_page='modify_login')

@users.route('/get_users', methods=['GET'])
@users.route('/get_users/<int:user_id>', methods=['GET'])
@login_required
def getEmployeesRoute(user_id=None):
    """
    Route to get all or specific user/s.
    Args:
        user_id (int, optional): User ID to get. If not provided, gets all users.
    """
    if request.method == 'GET':
        if current_user.admin:
            users = getUsers(user_id)
        else:
            users = getUsers(current_user.id)
        
        if users:
            return jsonify(users), 200
        else:
            return jsonify({"error": "No employees found"}), 404

@users.route('/get_users/is_registered/<int:employee_id>', methods=['GET'])
def getIsRegisteredRoute(employee_id):
    """
    Route to check if an employee id is already registered.
    Args:
        user_id (int): User ID to check.
    """
    if request.method == 'GET':
        registered = isEmployeeIdRegistered(employee_id)
        return jsonify({'registered': registered})

@users.route('/get_users/username_taken', methods=['GET'])
def getUsernameTakenRoute():
    """
    Route to check if a username is already registered.
    Args:
        username (str): Username to check.
    """
    if request.method == 'GET':
        username = request.args.get('username')
        taken = usernameTaken(username)
        return jsonify({'registered': taken})
    
@users.route('/add_user', methods=['POST'])
@login_required
@admin_required
def addUser():
    """
    Route to add a user from the modify login page
    """
    args = request.get_json()
    if (args):
        employee_id = args['employee_id']
        username = args['username']
        admin = args['admin']
        hashed_password = bcrypt.generate_password_hash(args['password']).decode('utf-8')

        register = registerUser({
            'employee_id': employee_id,
            'username': username,
            'hashed_password': hashed_password
        })

        user_id = register['pk_user_id']
        if admin == True:
            upgradeUser(user_id)
        
        if register['message'] == 'success':
            return jsonify({'message': 'success'})
        return jsonify({'message': 'error'})

@users.route('/promote_user/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def promoteUserRoute(user_id):
    """
    Route to promote a user from the modify login page
    """
    if request.method == 'PUT':
        upgrade = upgradeUser(user_id)
        if upgrade == 'success':
            return {'message': 'success'}
        else:
            return {'message': 'error'}
        
@users.route('/demote_user/<int:user_id>', methods=['PUT'])
@login_required
@admin_required
def demoteUserRoute(user_id):
    """
    Route to demote a user from the modify login page
    """
    if request.method == 'PUT':
        demote = demoteUser(user_id)
        if demote == 'success':
            return {'message': 'success'}
        else:
            return {'message': 'error'}

@users.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def deleteUserRoute(user_id):
    """
    Route to delete a user from the modify login page
    """
    if request.method == 'DELETE':
        delete = deleteUser(user_id)
        if delete == 'success':
            return {'message': 'success'}
        else:
            return {'message': 'error'}

@users.route('/change_password/<int:user_id>', methods=['PUT'])
@login_required
def changePasswordRoute(user_id):
    """
    Route to change a user password from the modify login page
    """
    if request.method == 'PUT':
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        change = changePassword(user_id, hashed_password)
        if change == 'success':
            return {'message': 'success'}
        else:
            return {'message': 'error'}

@users.route('/change_username/<int:user_id>', methods=['PUT'])
@login_required
def changeUsernameRoute(user_id):
    """
    Route to change a username from the modify login page
    """
    if request.method == 'PUT':
        data = request.get_json()
        username = data['username']

        change = changeUsername(user_id, username)
        if change == 'success':
            return {'message': 'success'}
        else:
            return {'message': 'error'}