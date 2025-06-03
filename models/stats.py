from db import get_db

def getStats(employee_id=None):
    """
    Get all employee's stats from the database or a specific employee by ID.
    Args:
        employee_id (int, optional): The ID of the employee to get.
    """
    try:
        # Create base query
        query = """
            SELECT * FROM EmployeeStats
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

