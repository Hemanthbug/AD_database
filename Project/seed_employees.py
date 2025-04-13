from faker import Faker
import mysql.connector
import random
from datetime import timedelta, date

fake = Faker()

# 📦 Connect to the EMS database
def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="hemanth",
        password="Hemanth",
        database="EMS",
        port=3306
    )

# 📌 Insert fake projects
def seed_projects(n=5):
    db = connect_db()
    cursor = db.cursor()
    for _ in range(n):
        name = fake.bs().title()
        desc = fake.text(100)
        start_date = fake.date_between(start_date='-1y', end_date='-3m')
        end_date = fake.date_between(start_date='-2m', end_date='+2m')
        status = random.choice(['Ongoing', 'Completed', 'Delayed'])
        cursor.execute("""
            INSERT INTO Projects (name, description, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, desc, start_date, end_date, status))
    db.commit()
    db.close()

# 👤 Insert fake employees linked to random projects
def seed_employees(n=200):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Projects")
    project_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        name = fake.name()
        department = random.choice(['IT', 'HR', 'Finance', 'Marketing'])
        role = random.choice(['Manager', 'Developer', 'Analyst', 'Intern'])
        email = fake.email()
        phone = fake.phone_number()[:30]
        address = fake.address().replace("\n", ", ")

        salary = round(random.uniform(40000, 120000), 2)
        bonus = round(random.uniform(1000, 10000), 2)
        perf_rating = random.randint(1, 5)
        working_days = random.randint(100, 250)
        project_id = random.choice(project_ids)

        cursor.execute("""
            INSERT INTO Employees (name, department, role, email, phone, address, salary, bonus,
                                   performance_rating, number_of_working_days, current_project_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (name, department, role, email, phone, address, salary, bonus,
              perf_rating, working_days, project_id))
    db.commit()
    db.close()

# ✅ Add fake tasks for employees
def seed_tasks():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Employees")
    employee_ids = [row[0] for row in cursor.fetchall()]

    for emp_id in employee_ids:
        for _ in range(random.randint(1, 3)):
            title = fake.catch_phrase()
            desc = fake.text(100)
            deadline = fake.date_between(start_date='today', end_date='+30d')
            status = random.choice(['Pending', 'In Progress', 'Completed'])
            cursor.execute("""
                INSERT INTO Tasks (employee_id, title, description, deadline, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (emp_id, title, desc, deadline, status))
    db.commit()
    db.close()

# 🕒 Add attendance records
def seed_attendance():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Employees")
    employee_ids = [row[0] for row in cursor.fetchall()]

    today = date.today()
    for emp_id in employee_ids:
        for i in range(5):  # last 5 days
            att_date = today - timedelta(days=i)
            status = random.choice(['Present', 'Absent'])
            cursor.execute("""
                INSERT INTO Attendance (employee_id, date, status)
                VALUES (%s, %s, %s)
            """, (emp_id, att_date, status))
    db.commit()
    db.close()

# 🌴 Add leave requests
def seed_leave_requests():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM Employees")
    employee_ids = [row[0] for row in cursor.fetchall()]

    for emp_id in random.sample(employee_ids, k=min(5, len(employee_ids))):
        from_date = fake.date_between(start_date='-1m', end_date='today')
        to_date = from_date + timedelta(days=random.randint(1, 5))
        reason = fake.sentence()
        status = random.choice(['Pending', 'Approved', 'Rejected'])

        cursor.execute("""
            INSERT INTO LeaveRequests (employee_id, from_date, to_date, reason, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (emp_id, from_date, to_date, reason, status))
    db.commit()
    db.close()

# 🎬 Run All Seeds
if __name__ == '__main__':
    seed_projects()
    seed_employees()
    seed_tasks()
    seed_attendance()
    seed_leave_requests()
    print("✅ All fake EMS data inserted successfully.")
