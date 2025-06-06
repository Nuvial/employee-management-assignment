from db import get_db

# Employee Table CRUD operations
def add_employee(data):
    """
    Add a new employee to the database.
    Args:
        data (dict): A dictionary containing employee details.
            Required keys include:
            'first_name'
            'last_name'
            'employee_position'
    Raises:
        KeyError: If any required keys are missing in the data.
        TypeError: If `data` is not a dictionary.
        Exception: For any other database-related errors.
    """

    try:
        # Store required data in variables
        first_name = data['first_name']
        last_name = data['last_name']
        position = data['employee_position']

        # Create query & set values
        query = """
            INSERT INTO Employees (first_name, last_name, employee_position)
            VALUES (?, ?, ?)
            """
        values = (first_name, last_name, position)

        # Execute the query
        db = get_db()
        cursor = db.execute(query, values)
        db.commit()
        new_id = cursor.lastrowid
        

        return {'status': 'success', 'employee_id': new_id}
    
    except KeyError as e:
        raise KeyError(f"Data must contain the key: {e}")
    except TypeError as e:
        raise TypeError(f"Data must be a dictionary: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

def get_employees(employee_id=None):
    """
    Get all employees from the database or a specific employee by ID.
    Args:
        employee_id (int, optional): The ID of the employee to get.
    """
    try:
        # Create base query
        query = """
            SELECT * FROM Employees
        """
        values = ()

        if (employee_id):
            # Add condition to base query if id is provided
            query += " WHERE pk_employee_id = ?"
            values = (employee_id,)
        
        # Execute the query
        db = get_db()
        employees_data = db.execute(query, values).fetchall()

        # Convert result into a dictionary
        employees_data = [dict(row) for row in employees_data]

        return employees_data
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def update_employee(employee_id, data):
    """
    Update an employee's details in the database.
    Args:
        employee_id (int): The ID of the employee to change.
        data (dict): A dictionary containing the employee fields to update.
            Valid keys include:
            'first_name'
            'last_name'
            'employee_position'
    """
    try:
        # Check if data is a dictionary
        if not isinstance(data, dict):
            raise TypeError('Data must be a dictionary.')

        # Define valid fields that can be updated
        valid_fields = [
            'first_name',
            'last_name',
            'employee_position'
        ]
        fields_to_update = []
        values = []

        # Check which fields are present in the data to update
        for key in valid_fields:
            if key in data:
                fields_to_update.append(f"{key} = ?")
                values.append(data[key])
        
        if not fields_to_update:
            raise ValueError('Data does not contain any valid fields to update.')

        # Create the SQL query to update the employee
        query = f"""
            UPDATE Employees
            SET {', '.join(fields_to_update)}
            WHERE pk_employee_id = ?        
        """
        values.append(employee_id)

        # Execute the query
        db = get_db()
        db.execute(query, values)
        db.commit()
        

        return 'success'
           
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def delete_employee(employee_id):
    """
    Delete an employee from the database.
    Args:
        employee_id (int): Employee ID to delete.
    """
    try:
        # Create query and set values
        query = """
            DELETE FROM Employees
            WHERE pk_employee_id = ?
        """
        values = (employee_id,)

        # Execute the query
        db = get_db()
        db.execute(query, values)
        db.commit()
        

        return 'success'

    except Exception as e:
        raise Exception(f"An error occurred: {e}")