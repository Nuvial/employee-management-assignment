from db import get_db

def getLeave(employee_id=None):
    """
    Get all employee's leave from the database or a specific employee by ID.
    Args:
        employee_id (int, optional): The ID of the employee to get.
    """
    try:
        # Create base query
        query = """
            SELECT * FROM EmployeeLeave
        """
        values = ()

        if (employee_id):
            # Add condition to base query if id is provided
            query += " WHERE pk_employee_id = ?"
            values = (employee_id,)
        
        # Execute the query
        db = get_db()
        stats = db.execute(query, values).fetchall()

        # Convert result into a dictionary
        stats = [dict(row) for row in stats]

        return stats
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def getRemainingLeave(employee_id=None):
    """
    Get the remaining sick and annual leave for a specific employee.
    Args:
        employee_id (int): The ID of the employee to get remaining leave for.
    """
    try:
        # Create query to get remaining leave
        query = """
            SELECT
                e.pk_employee_id as fk_employee_id,
                e.default_leave_balance -
                    IFNULL((
                        SELECT SUM(julianday(end_date) - julianday(start_date) + 1)
                        FROM EmployeeLeave
                        WHERE fk_employee_id = e.pk_employee_id
                        AND leave_type = 'Annual Leave'
                        AND (status = 'Approved' or status = 'Pending')
                        AND strftime('%Y', start_date) = strftime('%Y', 'now')
                    ), 0) AS leave_remaining,
                e.default_sick_leave_balance -
                    IFNULL((
                        SELECT SUM(julianday(end_date) - julianday(start_date) + 1)
                        FROM EmployeeLeave
                        WHERE fk_employee_id = e.pk_employee_id
                        AND leave_type = 'Sick Leave'
                        AND status = 'Approved'
                        AND strftime('%Y', start_date) = strftime('%Y', 'now')
                    ), 0) AS sick_leave_remaining
            FROM Employees e
        """
        values = ()

        if employee_id:
            # Add condition to base query if id is provided
            query += " WHERE e.pk_employee_id = ?"
            values = (employee_id,)

        # Execute the query
        db = get_db()
        stats = db.execute(query, values).fetchall()

        if stats:
            return [dict(row) for row in stats]
        else:
            return None
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
