from flask import request, jsonify, Blueprint, render_template
from flask_login import login_required

from .models.stats import getStats, updateStats, addStats

stats = Blueprint('stats', __name__)

@stats.route('/create/<int:employee_id>', methods=['POST'])
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