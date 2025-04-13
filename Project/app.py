from flask import Flask, render_template, request, redirect, url_for
import database

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('list_employees'))

@app.route('/employees')
def list_employees():
    employees = database.get_employees_with_project()
    return render_template('employees.html', employees=employees)

@app.route('/projects')
def list_projects():
    projects = database.get_projects()
    return render_template('projects.html', projects=projects)

@app.route('/tasks')
def list_tasks():
    tasks = database.get_tasks()
    return render_template('tasks.html', tasks=tasks)

  # ---------------------------------------
# Add New Employee
# ---------------------------------------
@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        database.add_employee(request.form)
        return redirect(url_for('list_employees'))
    return render_template('employee_form.html', employee=None)

# ---------------------------------------
# Edit Existing Employee
# ---------------------------------------
@app.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if request.method == 'POST':
        database.update_employee(id, request.form)
        return redirect(url_for('list_employees'))
    employee = database.get_employee(id)
    return render_template('employee_form.html', employee=employee)

# ---------------------------------------
# Delete Employee
# ---------------------------------------
@app.route('/employees/delete/<int:id>')
def delete_employee(id):
    database.delete_employee(id)
    return redirect(url_for('list_employees'))


@app.route('/attendance')
def list_attendance():
    attendance = database.get_attendance()
    return render_template('attendance.html', attendance=attendance)

@app.route('/leaves')
def list_leaves():
    leaves = database.get_leave_requests()
    return render_template('leaves.html', leaves=leaves)

if __name__ == '__main__':
    app.run(debug=True)


  