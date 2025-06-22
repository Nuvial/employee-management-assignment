from flask import request, jsonify, Blueprint, render_template
from flask_login import login_required, current_user

from .models.leave import getLeave, getRemainingLeave, getRequestedLeave, approveLeave, denyLeave, requestLeave
from .auth import admin_required

leave = Blueprint('leave', __name__)

@leave.route('/')
@login_required
def index():
    return render_template('process-leave.html', active_page='process_leave')


@leave.route('/get_leave', methods=['GET'])
@leave.route('/get_leave/<int:employee_id>', methods=['GET'])
@login_required
def getLeaveRoute(employee_id=None):
    """
    Route to get all or specific employee/s leave.
    Args:
        employee_id (int, optional): Employee ID to get. If not provided, gets all employees.
    """
    if request.method == 'GET':
        if current_user.admin:
            stats = getLeave(employee_id)
        else:
            stats = getLeave(current_user.employee_id)
        
        if stats:
            return jsonify(stats)
        else:
            return jsonify({"error": "No leave found"})

@leave.route('/get_leave/remaining', methods=['GET'])
@leave.route('/get_leave/remaining/<int:employee_id>', methods=['GET'])
@login_required
def getRemainingLeaveRoute(employee_id=None):
    """
    Route to get the remaining sick and annual leave for a specific employee.
    Args:
        employee_id (int): Employee ID to get remaining leave for.
    """
    if request.method == 'GET':
        if current_user.admin:
            stats = getRemainingLeave(employee_id)
        else:
            stats = getRemainingLeave(current_user.employee_id)
        
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No leave found"}), 404

@leave.route('/get_leave/requested', methods=['GET'])
@login_required
def getRequestedLeaveRoute():
    """
    Route to get employees with requested leave
    """
    if request.method == 'GET':
        if current_user.admin:
            employees = getRequestedLeave()
        else:
            employees = getRequestedLeave(current_user.employee_id)

        if employees:
            return jsonify(employees), 200
        else:
            return jsonify({"error": "No requested leave." })
        
@leave.route('/update_leave/approve/<int:leave_id>', methods=['PUT'])
@login_required
@admin_required
def approveLeaveRoute(leave_id):
    """
    Approves a specific leave id.
    Args:
        leave_id (int): Specific ID of the leave to approve.
        comment (str): Any admin comments.
    """
    if request.method == 'PUT':
        comments = request.get_json()['comment']
        approve = approveLeave(leave_id, comments)
        if approve == 'success':
            return {'data': 'success'}
        else:
            return jsonify({"error": "Could not approve leave." })
        
@leave.route('/update_leave/deny/<int:leave_id>', methods=['PUT'])
@login_required
@admin_required
def denyLeaveRoute(leave_id):
    """
    Denies a specific leave id.
    Args:
        leave_id (int): Specific ID of the leave to deny.
        comment (str): Any admin comments.
    """
    if request.method == 'PUT':
        comments = request.get_json()['comment']
        deny = denyLeave(leave_id, comments)
        if deny == 'success':
            return {'data': 'success'}
        else:
            return jsonify({"error": "Could not deny leave." })

@leave.route('/request_leave/', methods=['POST'])
@login_required
def requestLeaveRoute():
    """
    Route to request leave for the logged in user.
    """
    if request.method == 'POST':
        data = request.get_json()
        fk_employee_id = current_user.id
        leave_type = data['leave_type']
        start_date = data['start_date']
        end_date = data['end_date']
        comment_employee = data['employee_comments']

        leave_request = requestLeave(fk_employee_id, leave_type, start_date, end_date, comment_employee)
        if leave_request == 'success':
            return {'data': 'success'}
        else:
            return jsonify({"error": "Could not deny leave." })