-- Employees Table
CREATE TABLE Employees (
    pk_employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    default_leave_balance REAL NOT NULL DEFAULT 25, -- Base leave balance for all employees,
    default_sick_leave_balance REAL NOT NULL DEFAULT 5, -- Base sick leave balance for all employees
    employee_position TEXT NOT NULL  /* Team Lead, Developer, Designer, etc.
    Would ideally be stored in a lookup table, but assignment limits to 4 tables maximum. */
);

-- Employee Stats Table
CREATE TABLE EmployeeStats (
    pk_stat_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each stat entry, allows seeing the history of stats
    fk_employee_id INTEGER NOT NULL,
    attendance REAL NOT NULL,
    productivity REAL NOT NULL,
    performance REAL NOT NULL,
    date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_employee_id) REFERENCES Employees(pk_employee_id) ON DELETE CASCADE -- Ensures that if an employee is deleted, their stats are also deleted
);

-- Employee Leave Table
CREATE TABLE EmployeeLeave (
    pk_leave_id INTEGER PRIMARY KEY AUTOINCREMENT, -- Unique ID for each leave request, allows multiple leave requests per employee
    fk_employee_id INTEGER NOT NULL,
    leave_type TEXT NOT NULL, /* Sick Leave, Annual Leave, etc.
    Would ideally be stored in a lookup table, but assignment limits to 4 tables maximum. */
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    date_requested TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL, /* Draft, Pending, Approved, etc.
    Would ideally be stored in a lookup table, but assignment limits to 4 tables maximum. */
    FOREIGN KEY (fk_employee_id) REFERENCES Employees(pk_employee_id) ON DELETE CASCADE -- Ensures that if an employee is deleted, their leave requests are also deleted
);

-- Users Table
CREATE TABLE Users (
    pk_user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_employee_id INTEGER NOT NULL UNIQUE, -- Foreign key to Employees table, ensures each user is linked to an employee.
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL, -- Hashed password for security
    forgot_password BOOLEAN NOT NULL DEFAULT 0, -- Flag to indicate if the user has requested a password reset
    admin BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (fk_employee_id) REFERENCES Employees(pk_employee_id) ON DELETE CASCADE -- Ensures that if an employee is deleted, their account is also deleted.
);
