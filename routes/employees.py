from flask import Flask, request, jsonify, Blueprint

from models.employees import add_employee, get_employees, update_employee, delete_employee

employees = Blueprint('employees', __name__)

@employees.route('/get_employees', methods=['GET'])
def get_employees_route():
    """
    Route to get all or specific employee/s.
    """
    