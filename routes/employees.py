from flask import request, jsonify, Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from .models.employees import add_employee, get_employees, update_employee, delete_employee

employees = Blueprint('employees', __name__)

@employees.route('/')
@login_required
def index():
    return render_template('employees-view.html', active_page='view_records')

@employees.route('/modify')
@login_required
def modify_index():
    if not current_user.admin:
        flash('You need to be an admin to access this page.', 'danger')
        return redirect(url_for('employees.index', active_page='view_records'))
    return render_template('employees-modify.html', active_page='modify_records')

@employees.route('/get_employees', methods=['GET'])
@employees.route('/get_employees/<int:employee_id>', methods=['GET'])
def get_employees_route(employee_id=None):
    """
    Route to get all or specific employee/s.
    Args:
        employee_id (int, optional): Employee ID to get. If not provided, gets all employees.
    """
    if request.method == 'GET':
        employees_data = get_employees(employee_id)
        if employees_data:
            return jsonify(employees_data), 200
        else:
            return jsonify({"error": "No employees found"})


@employees.route('/add_employee', methods=['POST'])
def add_employee_route():
    """
    Route to add a new employee.
    Args:
        None (expects JSON payload in request body):
            - first_name (str): The employee's first name.
            - last_name (str): The employee's last name.
            - employee_position (str): The employee's position.
            - default_leave_balance (float/int): The base leave balance for the employee.
            - default_sick_leave_balance (float/int): The base sick leave balance for the employee.
    """
    if request.method == 'POST':
        employee_data = request.get_json()
        first_name = employee_data.get('first_name')
        last_name = employee_data.get('last_name')
        position = employee_data.get('employee_position')
        default_leave_balance = employee_data.get('default_leave_balance')
        default_sick_leave_balance = employee_data.get('default_sick_leave_balance')


        if not first_name or not last_name or not position or not default_leave_balance or not default_sick_leave_balance:
            return jsonify({"error": "Missing required fields"}), 400
        
        try: 
            status = add_employee(employee_data)
            if status['status'] == 'success':
                return jsonify({"message": "Employee added successfully", 'employee_id': status['employee_id']}), 201
            else:
                return jsonify({"error": "Failed to add employee"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@employees.route('/update_employee/<int:employee_id>', methods=['PUT'])
def update_employee_route(employee_id):
    """
    Route to update an existing employee.
    Args:
        employee_id (int): Employee ID to update.
    """
    if request.method == 'PUT':
        employee_data = request.get_json()
        try:
            status = update_employee(employee_id, employee_data)
            if status == 'success':
                return jsonify({"message": "Employee updated successfully"}), 200
            else:
                return jsonify({"error": "Failed to update employee"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@employees.route('/delete_employee/<int:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    """
    Route to delete an employee.
    Args:
        employee_id (int): Employee ID to delete.
    """
    if request.method == 'DELETE':
        try:
            status = delete_employee(employee_id)
            if status == 'success':
                return jsonify({"message": "Employee deleted successfully"}), 200
            else:
                return jsonify({"error": "Failed to delete employee"}), 500
        except Exception as e:
            return jsonify({"error": str(e)}), 500