from flask import Flask, render_template, request, redirect, url_for
import database  # Assuming your database.py is correctly handling DB operations

app = Flask(__name__)

# Redirect to the employee list page
@app.route('/')
def home():
    return redirect(url_for('list_employees'))  

# List all employees with project info
@app.route('/employees')
def list_employees():
    employees = database.get_employees_with_project()  # Fetch employees with project info
    return render_template('employees.html', employees=employees)

@app.route('/employees/search', methods=['GET', 'POST'])
def search_employee():
    search_done = False
    employee = None
    if request.method == 'GET' and request.args.get('emp_id'):
        emp_id = request.args.get('emp_id')
        # Search for the employee by ID
        employee = database.get_employee(int(emp_id))
        search_done = True

    # Pass the employee data and a flag to indicate whether the search was done
    return render_template('employees.html', employee=employee, search_done=search_done, employees=database.get_employees_with_project())


# Add New Employee
@app.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'department': request.form['department'],
            'role': request.form['role'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'address': request.form['address'],
            'salary': request.form['salary'],
            'bonus': request.form['bonus'],
            'performance_rating': request.form['performance_rating'],
            'number_of_working_days': request.form['number_of_working_days'],
            'current_project_id': request.form.get('current_project_id', None)  # Handle missing project ID
        }
        database.add_employee(data)  # Add employee to the database
        return redirect(url_for('list_employees'))
    return render_template('employee_form.html', employee=None)

# Edit Existing Employee - Step 1: Prompt for Employee ID
@app.route('/employees/edit', methods=['GET', 'POST'])
def prompt_employee_id():
    if request.method == 'POST':
        emp_id = request.form['employee_id']  # Get the ID entered by the user
        return redirect(url_for('edit_employee', id=emp_id))  # Redirect to the actual edit route with ID
    return render_template('employee_id_form.html')  # Render the form for entering the employee ID

# Edit Existing Employee - Step 2: Fetch employee data and update it
@app.route('/employees/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    employee = database.get_employee(id)  # Fetch the employee details using the ID

    if request.method == 'POST':
        updated_data = {
            'name': request.form.get('name', ''),
            'department': request.form.get('department', ''),
            'role': request.form.get('role', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),  # Safe handling of missing 'address'
            'salary': request.form.get('salary', ''),
            'bonus': request.form.get('bonus', ''),
            'performance_rating': request.form.get('performance_rating', ''),
            'number_of_working_days': request.form.get('number_of_working_days', ''),
            'current_project_id': request.form.get('current_project_id', None)  # Handle missing project ID
        }

        database.update_employee(id, updated_data)  # Update the employee's data in the database
        return redirect(url_for('list_employees'))  # Redirect to the employee list after update

    return render_template('edit_employee_form.html', employee=employee)  # Render the edit form with employee data

@app.route('/employees/delete', methods=['POST'])
def delete_employee_by_id():
    emp_id = request.form['emp_id']  # Get the selected employee ID from the form
    database.delete_employee(emp_id)  # Delete employee from the database
    return redirect(url_for('list_employees'))  # Redirect to the employee list after deletion


# List Attendance
@app.route('/attendance')
def list_attendance():
    attendance = database.get_attendance()
    return render_template('attendance.html', attendance=attendance)

# List Leave Requests
@app.route('/leaves')
def list_leaves():
    leaves = database.get_leave_requests()
    return render_template('leaves.html', leaves=leaves)

if __name__ == '__main__':
    app.run(debug=True)
