from flask import request, jsonify, Blueprint, render_template
from flask_login import login_required

from .models.stats import getStats

stats = Blueprint('stats', __name__)

# @stats.route('/')
# @login_required
# def index():
#     return render_template('employees-view.html', active_page='view_records')

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

