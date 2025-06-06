from flask import request, jsonify, Blueprint, render_template
from flask_login import login_required

from .models.leave import getLeave, getRemainingLeave

leave = Blueprint('leave', __name__)

# @stats.route('/')
# @login_required
# def index():
#     return render_template('employees-view.html', active_page='view_records')

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