from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from .models.leave import getLeave, getRemainingLeave, getRequestedLeave, approveLeave, denyLeave

leave = Blueprint('leave', __name__)

@leave.route('/')
@login_required
def index():
    if not current_user.admin:
        flash('You need to be an admin to access this page.', 'danger')
        return redirect(url_for('auth.dashboard', active_page='dashboard'))
    return render_template('process-leave.html', active_page='process_leave')


@leave.route('/get_leave', methods=['GET'])
@leave.route('/get_leave/<int:employee_id>', methods=['GET'])
def getLeaveRoute(employee_id=None):
    """
    Route to get all or specific employee/s leave.
    Args:
        employee_id (int, optional): Employee ID to get. If not provided, gets all employees.
    """
    if request.method == 'GET':
        stats = getLeave(employee_id)
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No leave found"}), 404

@leave.route('/get_leave/remaining', methods=['GET'])
@leave.route('/get_leave/remaining/<int:employee_id>', methods=['GET'])
def getRemainingLeaveRoute(employee_id=None):
    """
    Route to get the remaining sick and annual leave for a specific employee.
    Args:
        employee_id (int): Employee ID to get remaining leave for.
    """
    if request.method == 'GET':
        stats = getRemainingLeave(employee_id)
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No leave found"}), 404

@leave.route('/get_leave/requested', methods=['GET'])
def getRequestedLeaveRoute():
    """
    Route to get employees with requested leave
    """
    if request.method == 'GET':
        employees = getRequestedLeave()
        if employees:
            return jsonify(employees), 200
        else:
            return jsonify({"error": "No requested leave." })
        
@leave.route('/update_leave/approve/<int:leave_id>', methods=['PUT'])
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