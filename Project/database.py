import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="hemanth",
        password="Hemanth",
        database="EMS",
        port=3306
    )

def get_employees_with_project():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            e.id,
            e.name,
            e.department,
            e.role,
            e.email,
            e.phone,
            e.address,
            e.salary,
            e.bonus,
            e.performance_rating,
            e.number_of_working_days,
            p.name AS project_name,
            p.status AS project_status
        FROM Employees e
        LEFT JOIN Projects p ON e.current_project_id = p.id
    """)
    employees = cursor.fetchall()
    db.close()
    return employees

def get_projects():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Projects")
    result = cursor.fetchall()
    db.close()
    return result

def get_tasks():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, e.name AS employee_name
        FROM Tasks t
        JOIN Employees e ON t.employee_id = e.id
    """)
    result = cursor.fetchall()
    db.close()
    return result

def get_attendance():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, e.name AS employee_name
        FROM Attendance a
        JOIN Employees e ON a.employee_id = e.id
        ORDER BY date DESC
    """)
    result = cursor.fetchall()
    db.close()
    return result

def get_employee(emp_id):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Employees WHERE id = %s", (emp_id,))
    result = cursor.fetchone()
    db.close()
    return result

def add_employee(data):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Employees (name, department, role, email, phone, address, salary, bonus, performance_rating, number_of_working_days, current_project_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['name'], data['department'], data['role'], data['email'], data['phone'],
        data['address'], data['salary'], data['bonus'],
        data['performance_rating'], data['number_of_working_days'], data['current_project_id']
    ))
    db.commit()
    db.close()

def update_employee(emp_id, data):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE Employees
        SET name=%s, department=%s, role=%s, email=%s, phone=%s, address=%s,
            salary=%s, bonus=%s, performance_rating=%s, number_of_working_days=%s, current_project_id=%s
        WHERE id=%s
    """, (
        data['name'], data['department'], data['role'], data['email'], data['phone'],
        data['address'], data['salary'], data['bonus'],
        data['performance_rating'], data['number_of_working_days'], data['current_project_id'],
        emp_id
    ))
    db.commit()
    db.close()

def delete_employee(emp_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Employees WHERE id = %s", (emp_id,))
    db.commit()
    db.close()


def get_leave_requests():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT l.*, e.name AS employee_name
        FROM LeaveRequests l
        JOIN Employees e ON l.employee_id = e.id
        ORDER BY from_date DESC
    """)
    result = cursor.fetchall()
    db.close()

    return result