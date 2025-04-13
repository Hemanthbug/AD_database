-- Create the EMS database if not exists
CREATE DATABASE IF NOT EXISTS EMS;
USE EMS;

-- Drop old tables (safe if re-running script)
DROP TABLE IF EXISTS Tasks;
DROP TABLE IF EXISTS Attendance;
DROP TABLE IF EXISTS LeaveRequests;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Projects;

-- ✅ Create Projects Table
CREATE TABLE Projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50)
);

-- ✅ Create Employees Table
CREATE TABLE Employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(100),
    role VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(30),
    address TEXT,

    salary DECIMAL(10,2),
    bonus DECIMAL(10,2),
    performance_rating INT CHECK (performance_rating BETWEEN 1 AND 5),
    number_of_working_days INT,

    current_project_id INT,
    FOREIGN KEY (current_project_id) REFERENCES Projects(id)
);

-- ✅ Create Tasks Table
CREATE TABLE Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    title VARCHAR(255),
    description TEXT,
    deadline DATE,
    status VARCHAR(50),
    FOREIGN KEY (employee_id) REFERENCES Employees(id)
);

-- ✅ Create Attendance Table
CREATE TABLE Attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    date DATE,
    status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES Employees(id)
);

-- ✅ Create LeaveRequests Table
CREATE TABLE LeaveRequests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    from_date DATE,
    to_date DATE,
    reason TEXT,
    status VARCHAR(20),
    FOREIGN KEY (employee_id) REFERENCES Employees(id)
);
