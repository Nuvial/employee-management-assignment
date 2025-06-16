from db import get_db

def addStats(employee_id, data):
    """
    Create employee's stats details in the database.
    Args:
        employee_id (int): The ID of the employee to create.
        data (dict): A dictionary containing the stats fields.
            Valid keys include:
            'attendance'
            'productivity'
            'performance'
    """
    try:
        # Store required data in variables
        attendance = data['attendance']
        productivity = data['productivity']
        performance = data['performance']

        # Create query & set values
        query = """
            INSERT INTO EmployeeStats (fk_employee_id, attendance, productivity, performance, date_recorded)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """
        values = (employee_id, attendance, productivity, performance)

        # Execute the query
        db = get_db()
        db.execute(query, values)
        db.commit()

        return {'status': 'success'}


    except KeyError as e:
        raise KeyError(f"Data must contain the key: {e}")
    except TypeError as e:
        raise TypeError(f"Data must be a dictionary: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

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

def updateStats(employee_id, data):
    """
    Update an employee's stats details in the database.
    Args:
        employee_id (int): The ID of the employee to change.
        data (dict): A dictionary containing the stats fields to update.
            Valid keys include:
            'attendance'
            'productivity'
            'performance'
    """
    try:
        # Check if data is a dictionary
        if not isinstance(data, dict):
            raise TypeError('Data must be a dictionary.')

        # Define valid fields that can be updated
        valid_fields = [
            'attendance',
            'productivity',
            'performance'
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

        # Add timestamp
        fields_to_update.append('date_recorded = CURRENT_TIMESTAMP')

        # Create the SQL query to update the employee
        query = f"""
            UPDATE EmployeeStats
            SET {', '.join(fields_to_update)}
            WHERE fk_employee_id = ?        
        """
        values.append(employee_id)

        # Execute the query
        db = get_db()
        db.execute(query, values)
        db.commit()
        

        return 'success'
           
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


# -------------------------- Attendance/Performance Models ------------------------------
class Averages:
    def __init__(self, average):
        # set up a connection.
        self.db = get_db()
        if average not in ("attendance", "performance"):
            raise ValueError('Average must be "attendance" or ')
        self.column = average
    
    def top5(self):
        try:
            #Create query
            query = f"""
                SELECT fk_employee_id, {self.column} 
                FROM EmployeeStats
                ORDER BY attendance DESC
                LIMIT 5;
            """
            output = self.db.execute(query).fetchall()

            #Convert output to dict
            return [dict(i) for i in output]

        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def bottom5(self):
        try:
            #Create query
            query = f"""
                SELECT fk_employee_id, {self.column}  
                FROM EmployeeStats
                ORDER BY {self.column} ASC
                LIMIT 5;
            """
            output = self.db.execute(query).fetchall()

            #Convert output to dict
            return [dict(i) for i in output]

        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def mean(self):
        try: 
            #Create query
            query = f"""
                SELECT
                    fk_employee_id,
                    (SELECT AVG({self.column}) from EmployeeStats) AS mean_{self.column} 
                FROM EmployeeStats
                WHERE {self.column} <= (SELECT AVG({self.column}) FROM EmployeeStats)
            """

            output = self.db.execute(query).fetchall()

            #Convert output to dict
            return [dict(i) for i in output]
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def median(self):
        try: 
            #Create query
            query = f"""
                SELECT 
                    fk_employee_id,
                    (SELECT AVG({self.column}) FROM (
                            SELECT {self.column}
                            FROM EmployeeStats
                            ORDER BY {self.column}
                            LIMIT 2 - (SELECT COUNT(*) FROM EmployeeStats) % 2
                            OFFSET (SELECT (COUNT(*) - 1) / 2 FROM EmployeeStats)
                        )
                    ) as median_{self.column}
                FROM EmployeeStats
                WHERE {self.column} < (
                    SELECT
                        AVG({self.column})
                    FROM (
                        SELECT {self.column}
                        FROM EmployeeStats
                        ORDER BY {self.column}
                        LIMIT 2 - (SELECT COUNT(*) FROM EmployeeStats) % 2
                        OFFSET (SELECT (COUNT(*) - 1) / 2 FROM EmployeeStats)
                    )
                )
            """

            output = self.db.execute(query).fetchall()

            #Convert output to dict
            return [dict(i) for i in output]
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def range(self):
        try: 
            #Create query
            query = f"""
            SELECT fk_employee_id, range_{self.column} FROM (
                SELECT 
                    fk_employee_id,
                    (SELECT MAX({self.column}) FROM EmployeeStats) - (SELECT MIN({self.column}) FROM EmployeeStats) AS range_{self.column}
                FROM EmployeeStats
                WHERE {self.column} = (SELECT MAX({self.column}) FROM EmployeeStats)
                LIMIT 1
            )
            UNION ALL
            SELECT fk_employee_id, range_{self.column} FROM (
                SELECT 
                    fk_employee_id, 
                    (SELECT MAX({self.column}) FROM EmployeeStats) - (SELECT MIN({self.column}) FROM EmployeeStats) AS range_{self.column}
                FROM EmployeeStats
                WHERE {self.column} = (SELECT MIN({self.column}) FROM EmployeeStats)
                LIMIT 1
            )
        """

            output = self.db.execute(query).fetchall()

            #Convert output to dict
            return [dict(i) for i in output]
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
    
    def modal(self):
        try: 
            #Create query
            query = f"""
                WITH mode_{self.column} AS (
                    SELECT {self.column}
                    FROM EmployeeStats
                    GROUP BY {self.column}
                    HAVING COUNT(*) = (
                        SELECT MAX(cnt)
                        FROM (
                            SELECT COUNT(*) AS cnt
                            FROM EmployeeStats
                            GROUP BY {self.column}
                        )
                    )
                    ORDER BY {self.column} ASC
                    LIMIT 1
                )
                SELECT fk_employee_id, {self.column} as modal_{self.column}
                FROM EmployeeStats
                WHERE {self.column} = (SELECT {self.column} FROM mode_{self.column})
            """

            output = self.db.execute(query).fetchall()

            #Convert output to dict
            return [dict(i) for i in output]
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
