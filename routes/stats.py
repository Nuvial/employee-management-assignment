from flask import request, jsonify, Blueprint, render_template
from flask_login import login_required

from .models.stats import getStats, updateStats, addStats, Averages
from .auth import admin_required

stats = Blueprint('stats', __name__)

@stats.route('/create/<int:employee_id>', methods=['POST'])
@login_required
@admin_required
def createStatsRoute(employee_id):
    """
    Route to add a new employee.
    Args:
        employee_id (int): Employee ID to create stats for.
        None (expects JSON payload in request body):
            - attendance (float): Attendance as a float 0 - 100.
            - productivity (float): Productivity as a float from 0 - 100.
            - performance (float): Performance as a float from 0 - 10.
    """
    if request.method == 'POST':
        employee_data = request.get_json()
        attendance = employee_data.get('attendance')
        productivity = employee_data.get('productivity')
        performance = employee_data.get('performance')

        if not attendance or not productivity or not performance:
            return jsonify({"error": "Missing required fields"}), 400
        
        try: 
            status = addStats(employee_id, employee_data)
            if status['status'] == 'success':
                return jsonify({"message": "Employee stats added successfully"}), 201
            else:
                return jsonify({"error": "Failed to add employee stats"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@stats.route('/get_stats', methods=['GET'])
@stats.route('/get_stats/<int:employee_id>', methods=['GET'])
@login_required
def getStatsRoute(employee_id=None):
    """
    Route to get all or specific employee/s statistics.
    Args:
        employee_id (int, optional): Employee ID to get. If not provided, gets all employees.
    """
    if request.method == 'GET':
        stats = getStats(employee_id)
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/update/<int:employee_id>', methods=['PUT'])
@login_required
@admin_required
def updateStatsRoute(employee_id):
    """
    Route to update an existing employee's stats.
    Args:
        employee_id (int): Employee ID to update.
    """
    if request.method == 'PUT':
        data = request.get_json()
        try:
            status = updateStats(employee_id, data)
            if status == 'success':
                return jsonify({"message": "Employees stats updated successfully"}), 200
            else:
                return jsonify({"error": "Failed to update employee"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500



# --------------- Averages Routes ----------------

@stats.route('/attendance/top5', methods=['GET'])
@login_required
@admin_required
def getAttendanceTop5():
    """
    Route to get top 5 attendance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        attendance = Averages('attendance')
        stats = attendance.top5()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/attendance/bottom5', methods=['GET'])
@login_required
@admin_required
def getAttendanceBottom5():
    """
    Route to get bottom 5 attendance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        attendance = Averages('attendance')
        stats = attendance.bottom5()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/attendance/mean', methods=['GET'])
@login_required
@admin_required
def getAttendanceMean():
    """
    Route to get mean attendance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        attendance = Averages('attendance')
        stats = attendance.mean()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/attendance/median', methods=['GET'])
@login_required
@admin_required
def getAttendanceMedian():
    """
    Route to get median attendance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        attendance = Averages('attendance')
        stats = attendance.median()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/attendance/range', methods=['GET'])
@login_required
@admin_required
def getAttendanceRange():
    """
    Route to get range attendance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        attendance = Averages('attendance')
        stats = attendance.range()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/attendance/modal', methods=['GET'])
@login_required
@admin_required
def getAttendanceModal():
    """
    Route to get modal attendance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        attendance = Averages('attendance')
        stats = attendance.modal()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/performance/top5', methods=['GET'])
@login_required
@admin_required
def getPerformanceTop5():
    """
    Route to get top 5 performance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        performance = Averages('performance')
        stats = performance.top5()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/performance/bottom5', methods=['GET'])
@login_required
@admin_required
def getPerformanceBottom5():
    """
    Route to get bottom 5 performance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        performance = Averages('performance')
        stats = performance.bottom5()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/performance/mean', methods=['GET'])
@login_required
@admin_required
def getPerformanceMean():
    """
    Route to get mean performance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        performance = Averages('performance')
        stats = performance.mean()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/performance/median', methods=['GET'])
@login_required
@admin_required
def getPerformanceMedian():
    """
    Route to get median performance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        performance = Averages('performance')
        stats = performance.median()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/performance/range', methods=['GET'])
@login_required
@admin_required
def getPerformanceRange():
    """
    Route to get range performance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        performance = Averages('performance')
        stats = performance.range()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404

@stats.route('/performance/modal', methods=['GET'])
@login_required
@admin_required
def getPerformanceModal():
    """
    Route to get modal performance employee id's
    Returns:
        employee_id (array): A list of employee ID's.
    """
    if request.method == 'GET':
        performance = Averages('performance')
        stats = performance.modal()
        if stats:
            return jsonify(stats), 200
        else:
            return jsonify({"error": "No stats found"}), 404