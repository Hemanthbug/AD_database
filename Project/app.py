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
        try:
            # Collect data from the form
            data = {
                'name': request.form.get('name', ''),
                'department': request.form.get('department', ''),
                'role': request.form.get('role', ''),
                'email': request.form.get('email', ''),
                'phone': request.form.get('phone', ''),
                'address': request.form.get('address', ''),
                'salary': float(request.form.get('salary', 0.0)),  # Convert to float
                'bonus': float(request.form.get('bonus', 0.0)),
                'performance_rating': int(request.form.get('performance_rating', 0)),
                'number_of_working_days': int(request.form.get('number_of_working_days', 0)),
                'current_project_id': request.form.get('current_project_id'),
                'project_name': request.form.get('project_name', ''),  # Get project name from the form
                'project_status': request.form.get('project_status', '')  # Get project status from the form
            }

            # Handle case where current_project_id is not provided
            if not data['current_project_id']:
                data['current_project_id'] = None
            else:
                data['current_project_id'] = int(data['current_project_id'])

            database.add_employee(data)  # Add employee to the database

            return redirect(url_for('list_employees'))  # Redirect to the employee list

        except Exception as e:
            print("Error while adding employee:", e)  # Debugging output
            return "Internal Server Error: " + str(e), 500

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
            'salary': float(request.form.get('salary', 0.0)),  # Convert to float
            'bonus': float(request.form.get('bonus', 0.0)),
            'performance_rating': int(request.form.get('performance_rating', 0)),
            'number_of_working_days': int(request.form.get('number_of_working_days', 0)),
            'current_project_id': request.form.get('current_project_id', None),  # Handle missing project ID
            'project_name': request.form.get('project_name', ''),  # Get project name from the form
            'project_status': request.form.get('project_status', '')  # Get project status from the form
        }

        # Handle case where current_project_id is not provided
        if not updated_data['current_project_id']:
            updated_data['current_project_id'] = None
        else:
            updated_data['current_project_id'] = int(updated_data['current_project_id'])

        database.update_employee(id, updated_data)  # Update the employee's data in the database
        return redirect(url_for('list_employees'))  # Redirect to the employee list after update

    return render_template('edit_employee_form.html', employee=employee)  # Render the edit form with employee data


@app.route('/employees/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    # Assuming 'database' is a module handling DB operations
    employee = database.get_employee(id)  # Fetch the employee by ID
    if employee:
        database.delete_employee(id)  # Delete the employee from the database
        return redirect(url_for('list_employees'))  # Redirect to the employee list page
    return redirect(url_for('list_employees'))  # Handle case if employee is not found

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
