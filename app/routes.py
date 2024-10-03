from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Employee, Status, Position, Department
from app import db

#Utility
from app.validators import *

main = Blueprint('main', __name__)

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#api for register account
@main.route('/api/register', methods=['POST'])
def api_create_user():
    # Get data from the request (JSON payload)
    data = request.get_json()


    # Extract username and password
    username = data.get('username')
    password = data.get('password')

    # Validate that both fields are provided
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    # Create and save the new user
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    logout_user()

    return jsonify({"message": "User created successfully!"}), 201

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            #return redirect(url_for('main.login'))
            return f'''<p>Logged in as: {current_user.username}</p>
                       <form action="{url_for('main.logout')}" method="POST">
                       <button type="submit">Logout</button>
                       </form>
                    '''
        flash('Invalid credentials')
        return render_template('login.html', error_message='Invalid credentials'), 401
    return render_template('login.html'), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    # return redirect(url_for('main.login'))
    return render_template('login.html', message='Logout successfully'), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/status', methods=['POST','GET'])
@login_required
def status_post_get():
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data from the request

        # Check if 'name' is provided in the request
        if not data or not 'name' in data:
            return jsonify({"error": "Status name is required"}), 400
        status_name = data['name']

        # Validate the status_name with a minimum length of 1 and a maximum length of 100 (default)
        if not is_valid_name(status_name):
            return jsonify({"error": "Invalid status name. Must be between 1 and 100 characters long, alphanumeric."}), 400

        # Check if status with the same name already exists
        existing_status = Status.query.filter_by(status_name=status_name).first()
        if existing_status:
            return jsonify({"error": "Status already exists"}), 400
        
        # Create the new status
        new_status = Status(status_name=status_name)
        db.session.add(new_status)
        db.session.commit()
        
        return jsonify({"message": "Status created successfully", "status": status_name}), 201
    
    elif request.method == 'GET':

        # Query all statuses from the database
        statuses = Status.query.all()

        # Convert each status to a dictionary
        status_list = [{"id": status.id, "name": status.status_name} for status in statuses]

        # Return the list of statuses as JSON
        return jsonify({"statuses": status_list}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/status/<int:status_id>', methods=['DELETE','PATCH','PUT'])
@login_required
def status_delete_patch_put(status_id):
    # status id 1 or "Deleted" preserved as deletion marker
    #check of status_id = 1 denied delete access
    if status_id == 1:
        return jsonify({"error": "Status ID 1 is perserved you are not allow to modify or delete this status"}), 401
    if request.method == 'DELETE':
        # Find the status by ID
        status = Status.query.get(status_id)

        #If not found
        if not status:
            return jsonify({"error": "Status not found"}), 404

        # Check if any employees are using this status
        employees_with_status = Employee.query.filter_by(status_id=status_id).all()
        if employees_with_status:
            # Create a list of employees with their id and name
            employee_list = [{"id":employee.id, "name": employee.name} for employee in employees_with_status]
            return jsonify({
                "error": "Cannot delete status. There are employees associated with this status.",
                "employee_count": len(employees_with_status),
                "employees": employee_list
            }), 400

        # If no employees are associated with this status, proceed with deletion
        db.session.delete(status)
        db.session.commit()

        return jsonify({"message": "Status deleted successfully"}), 200
    else:
        #for method "PATCH" "PUT" (Only status will have "PATCH" method since for this case it is same as "PATCH")

        # Get the new status name from the request body
        data = request.get_json()

        if not data or not 'name' in data:
            return jsonify({"error": "New status name is required"}), 400

        new_name = data['name']

        # Validate the status_name with a minimum length of 1 and a maximum length of 100 (default)
        if not is_valid_name(new_name):
            return jsonify({"error": "Invalid status name. Must be between 1 and 100 characters long, alphanumeric."}), 400

        # Find the status by ID
        status = Status.query.get(status_id)

        if not status:
            return jsonify({"error": "Status not found"}), 404

        # Check if another status with the same name already exists
        existing_status = Status.query.filter_by(status_name=new_name).first()
        if existing_status and existing_status.id != status_id:
            return jsonify({"error": "Another status with this name already exists"}), 400

        # Update the status name
        status.status_name = new_name
        db.session.commit()

        return jsonify({"message": "Status updated successfully", "status": {"id": status.id, "name": status.status_name}}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/position', methods=['POST','GET'])
@login_required
def position_post_get():
    if request.method == 'POST':
        # Get the input data from the request body
        data = request.get_json()

        # Validate the required fields
        if not data or 'name' not in data or 'salary' not in data:
            return jsonify({"error": "Position name and salary are required"}), 400

        position_name = data['name']
        salary = data['salary']

        # Validate position name (length between 1 and 100 default)
        if not is_valid_name(position_name):
            return jsonify({"error": "Invalid position name. Must be between 1 and 100 characters long, alphanumeric."}), 400

        # Validate salary (must be a positive number)
        if not is_valid_salary(salary):
            return jsonify({"error": "Invalid salary. Must be a positive number."}), 400

        # Check if the position with the same name already exists
        existing_position = Position.query.filter_by(position_name=position_name).first()
        if existing_position:
            return jsonify({"error": "A position with this name already exists"}), 400

        # Create and save the new position
        new_position = Position(position_name=position_name, salary=salary)
        db.session.add(new_position)
        db.session.commit()

        return jsonify({"message": "Position created successfully", "position": {"id": new_position.id, "name": new_position.position_name, "salary": new_position.salary}}), 201
    
    elif request.method == 'GET':
        # Query all positions from the database
        positions = Position.query.all()

        # Convert each position to a dictionary
        position_list = [{"id": position.id, "name": position.position_name, "salary": position.salary} for position in positions]

        # Return the list of positions as JSON
        return jsonify({"positions": position_list}), 200
    
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/position/<int:position_id>', methods=['PATCH','DELETE'])
@login_required
def position_patch_delete(position_id):
    if request.method == 'PATCH':
        # Get the input data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Find the position by ID
        position = Position.query.get(position_id)

        if not position:
            return jsonify({"error": "Position not found"}), 404

        # Update name if provided and valid
        if 'name' in data:
            new_name = data['name']
            if not is_valid_name(new_name):
                return jsonify({"error": "Invalid position name. Must be between 1 and 100 characters long, alphanumeric."}), 400
            
            # Check if another position with the same name already exists
            existing_position = Position.query.filter_by(position_name=new_name).first()
            if existing_position and existing_position.id != position_id:
                return jsonify({"error": "Another position with this name already exists"}), 400
            
            position.position_name = new_name

        # Update salary if provided and valid
        if 'salary' in data:
            new_salary = data['salary']
            if not is_valid_salary(new_salary):
                return jsonify({"error": "Invalid salary. Must be a positive number."}), 400
            
            position.salary = new_salary

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Position updated successfully", "position": {"id": position.id, "name": position.position_name, "salary": position.salary}}), 200
    
    elif request.method == 'DELETE':
        # Find the position by ID
        position = Position.query.get(position_id)

        if not position:
            return jsonify({"error": "Position not found"}), 404

        # Check if there are any employees associated with this position
        employees_with_position = Employee.query.filter_by(position_id=position_id).all()

        if employees_with_position:
            # Create a list of employees with their id and name
            employee_list = [{"id":employee.id, "name": employee.name} for employee in employees_with_position]
            return jsonify({
                "error": "Cannot delete position. There are employees associated with this position.",
                "employee_count": len(employees_with_position),
                "employees": employee_list
            }), 400

        # If no employees are associated, proceed with deletion
        db.session.delete(position)
        db.session.commit()

        return jsonify({"message": "Position deleted successfully"}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/department', methods=['POST','GET'])
@login_required
def department_post_get():
    if request.method == 'POST':
        # Get the input data from the request body
        data = request.get_json()

        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Department name is required"}), 400

        department_name = data['name']
        manager_id = data.get('manager_id')  # Optional field

        # Validate the department name
        if not is_valid_name(department_name, length_from=3, length_to=100):
            return jsonify({"error": "Invalid department name. Must be between 3 and 100 characters long, alphanumeric."}), 400

        # Check if manager_id is provided and valid
        if manager_id:
            manager = Employee.query.get(manager_id)
            if not manager:
                return jsonify({"error": "Manager with the given ID not found"}), 404
            if manager.manager == False:
                return jsonify({"error": "This employee cannot be assigned as department manager because he/she isn't a manager"}), 409
        else:
            manager_id = None  # If no manager is provided, set manager_id to None

        # Check if status with the same name already exists
        existing_department = Department.query.filter_by(department_name=department_name).first()
        if existing_department:
            return jsonify({"error": "Department name already exists"}), 400

        # Create and save the new department
        new_department = Department(department_name=department_name, manager_id=manager_id)
        db.session.add(new_department)
        db.session.commit()

        return jsonify({"message": "Department created successfully", "department": {"id": new_department.id, "department_name": new_department.department_name, "manager_id": new_department.manager_id}}), 201
    elif request.method == 'GET':
        # Query all departments from the database
        departments = Department.query.all()

        # Convert each department to a dictionary with manager details (if any)
        department_list = []
        for department in departments:
            manager = None
            if department.manager_id:
                manager_obj = Employee.query.get(department.manager_id)
                manager = {"id": manager_obj.id, "name": manager_obj.name} if manager_obj else None
            
            department_list.append({
                "id": department.id,
                "department_name": department.department_name,
                "manager": manager
            })

        # Return the list of departments as JSON
        return jsonify({"departments": department_list}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/department/<int:department_id>', methods=['PATCH','DELETE'])
@login_required
def department_patch_delete(department_id):
    if request.method == 'PATCH':
        # Get the input data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Find the department by ID
        department = Department.query.get(department_id)

        if not department:
            return jsonify({"error": "Department not found"}), 404

        # Update department name if provided and valid
        if 'name' in data:
            new_department_name = data['name']
            if not is_valid_name(new_department_name, length_from=3, length_to=100):
                return jsonify({"error": "Invalid department name. Must be between 3 and 100 characters long, alphanumeric."}), 400
            
            department.department_name = new_department_name

        # Update manager_id if provided and valid
        if 'manager_id' in data:
            new_manager_id = data['manager_id']
            
            if new_manager_id:  # If manager_id is provided and not null
                manager = Employee.query.get(new_manager_id)
                if not manager:
                    return jsonify({"error": "Manager with the given ID not found"}), 404
                if manager.manager == False:
                    return jsonify({"error": "This employee cannot be assigned as department manager because he/she isn't a manager"}), 409
                department.manager_id = new_manager_id
            else:
                # If manager_id is null or empty, remove the manager from the department
                department.manager_id = None

        # Commit the changes to the database
        db.session.commit()

        return jsonify({"message": "Department updated successfully", "department": {"id": department.id, "department_name": department.department_name, "manager_id": department.manager_id}}), 200
    
    elif request.method == 'DELETE':
        # Find the department by ID
        department = Department.query.get(department_id)

        if not department:
            return jsonify({"error": "Department not found"}), 404

        # Check if there are any employees associated with this department
        employees_in_department = Employee.query.filter_by(department_id=department_id).all()

        if employees_in_department:
            # Create a list of employees with their id and name
            employee_list = [{"id": manager.id, "name": manager.name} for manager in employees_in_department]
            return jsonify({
                "error": "Cannot delete department. There is a manager associated with this department.",
                "manager": employee_list
            }), 400

        # If no employees are associated, proceed with deletion
        db.session.delete(department)
        db.session.commit()

        return jsonify({"message": "Department deleted successfully"}), 200
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/employee', methods=['POST','GET'])
@login_required
def employee_post_get():
    if request.method == 'POST':
        # Get the input data from the request body
        data = request.get_json()

        # Validate required fields
        # The following parameter should be in initial create employee:
        # • Name
        # • Address
        # • Status ID (Should exist)
        # • Department ID (Should exist)
        # • Position ID (Should exist)
        if not data or 'name' not in data or 'address' not in data or 'status_id' not in data or 'position_id' not in data or 'department_id' not in data:
            return jsonify({"error": "Name, address, status, position, and department are required"}), 400

        name = data['name']
        address = data['address']
        status_id = data['status_id']
        department_id = data['department_id']
        position_id = data['position_id']
        manager = data.get('manager', False)  # Optional field, defaults to False
        image_path = data.get('image_path')  # Optional field

        # Validate the employee name
        if not is_valid_name(name, length_from=4, length_to=150):
            return jsonify({"error": "Invalid name. Must be between 4 and 150 characters long, alphanumeric."}), 400

        # Validate the employee address
        if not is_valid_address(address):
            return jsonify({"error": "Invalid address. Must be between 1 and 400 characters long, alphanumeric."}), 400

        # Validate that the status, department, position should exist
        status = Status.query.get(status_id)
        if not status:
            return jsonify({"error": "Status not found"}), 404

        department = Department.query.get(department_id)
        if not department:
            return jsonify({"error": "Department not found"}), 404
        
        position = Position.query.get(position_id)
        if not position:
            return jsonify({"error": "Position not found"}), 404

        # Validate that the manager field is a boolean
        if not isinstance(manager, bool):
            return jsonify({"error": "Manager must be a boolean value (True or False)"}), 400

        # Validate image_path if provided
        if image_path and not is_valid_url(image_path):
            return jsonify({"error": "Invalid image URL or URL are too long (more than 2000 characters)"}), 400

        # Create and save the new employee
        new_employee = Employee(
            name=name, 
            address=address, 
            manager=manager,  # Boolean value for manager
            status_id=status_id, 
            position_id=position_id, 
            department_id=department_id, 
            image=image_path  # Use image_path if provided
        )
        db.session.add(new_employee)
        db.session.commit()

        return jsonify({
            "message": "Employee created successfully", 
            "employee": {
                "id": new_employee.id, 
                "name": new_employee.name, 
                "position": position.position_name,  # Access related position
                "department_id": department.department_name,  # Access related department
                "status_id": status.status_name,  # Access related status
                "manager": new_employee.manager,
                "image_path": new_employee.image
            }
        }), 201
    
    elif request.method == 'GET':
       # Query all employees with their related position, department, and status information
        employees = db.session.query(
            Employee.id,
            Employee.name,
            Employee.address,
            Employee.manager,
            Employee.image,  # Use 'image' instead of 'image_path'
            Position.position_name,
            Department.department_name,
            Status.status_name
        ).join(Position, Employee.position_id == Position.id)\
        .join(Department, Employee.department_id == Department.id)\
        .join(Status, Employee.status_id == Status.id)\
        .all()

        # Convert the result to a list of dictionaries with keys in desired order
        employee_list = [
            {
                "id": employee.id,
                "name": employee.name,
                "address": employee.address,
                "manager": employee.manager,
                "image": employee.image,  # Return 'image'
                "position": employee.position_name,
                "department": employee.department_name,
                "status": employee.status_name
            }
            for employee in employees
        ]

        # Return the list of employees as JSON
        return jsonify({"employees": employee_list}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/employee/<int:employee_id>', methods=['PATCH', 'DELETE'])
@login_required
def employee_patch_delete(employee_id):
    if request.method == 'PATCH':
        # Get the employee by ID
        employee = Employee.query.get(employee_id)
        
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        # Get the input data from the request body
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Update the employee's name if provided and valid
        if 'name' in data:
            new_name = data['name']
            if not is_valid_name(new_name, 4, 150):
                return jsonify({"error": "Invalid name. Must be between 4 and 150 characters long."}), 400
            employee.name = new_name

        # Update the address if provided and valid
        if 'address' in data:
            new_address = data['address']
            if not is_valid_address(new_address):
                return jsonify({"error": "Invalid address. Must be between 1 and 400 characters long."}), 400
            employee.address = new_address

        # Update the status if provided and valid
        if 'status_id' in data:
            new_status_id = data['status_id']
            status = Status.query.get(new_status_id)
            if not status:
                return jsonify({"error": "Status not found"}), 404
            employee.status_id = new_status_id

        # Update the position if provided and valid
        if 'position_id' in data:
            new_position_id = data['position_id']
            position = Position.query.get(new_position_id)
            if not position:
                return jsonify({"error": "Position not found"}), 404
            employee.position_id = new_position_id

        # Update the department if provided and valid
        if 'department_id' in data:
            new_department_id = data['department_id']
            department = Department.query.get(new_department_id)
            if not department:
                return jsonify({"error": "Department not found"}), 404
            employee.department_id = new_department_id

        # Update the manager field if provided and valid (boolean)
        if 'manager' in data:
            new_manager = data['manager']
            if not isinstance(new_manager, bool):
                return jsonify({"error": "Manager must be a boolean value (True or False)."}), 400
            employee.manager = new_manager

        # Update the image if provided and valid
        if 'image_path' in data:
            new_image = data['image_path']
            if not is_valid_url(new_image):
                return jsonify({"error": "Invalid image URL."}), 400
            employee.image = new_image

        # Commit the changes to the database
        db.session.commit()

        # Get Recent Info about status, department, and position
        status = Status.query.get(employee.status_id)
        department = Department.query.get(employee.department_id)
        position = Position.query.get(employee.position_id)

        # Return the updated employee information
        return jsonify({
            "message": "Employee updated successfully",
            "employee": {
                "id": employee.id,
                "name": employee.name,
                "address": employee.address,
                "manager": employee.manager,
                "image": employee.image,
                "status": status.status_name,
                "department": department.department_name,
                "position": position.position_name
            }
        }), 200
    elif request.method == 'DELETE':
        #Prevent deletion Strategy: Delete by as status "Deleted"
        # **IF you would like to permanent delete please using the next function
        # path = "/api/employee/<int:employee_id>/permanent"

        # Find the employee by ID
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({"error": "Employee not found"}), 404

        related_department = Department.query.filter_by(manager_id=employee_id).first()
        if related_department:
            return jsonify({"error": "This employee is a manager of department id: "+str(related_department.id)+"please remove or replace him/her from the department first"}), 400

        # Update the employee status to 'Deleted'
        deleted_status = Status.query.filter_by(status_name='Deleted').first()
        if not deleted_status:
            return jsonify({"error": "Deleted status not found"}), 500

        if employee.status_id == 1:
            return jsonify({"error": "This employee is already marked as Deleted"}), 409

        # Set the employee status to 'Deleted'
        employee.status_id = deleted_status.id
        db.session.commit()

        return jsonify({"message": "Employee marked as deleted successfully"}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@main.route('/api/employee/<int:employee_id>/permanent', methods=['DELETE'])
@login_required
def employee_permanent_delete(employee_id):
    # Find the employee by ID
    employee = Employee.query.get(employee_id)

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    related_department = Department.query.filter_by(manager_id=employee_id).first()
    if related_department:
        return jsonify({"error": "This employee is a manager of department id: "+str(related_department.id)+" , please remove or replace him/her from the department first"}), 400

    # Delete the employee from the database
    db.session.delete(employee)
    db.session.commit()

    return jsonify({"message": "Employee deleted successfully"}), 200

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@main.route('/api/employees')
@login_required
def employees():
    position_id = request.args.get('position')
    department_id = request.args.get('department')
    status_id = request.args.get('status')

    employees = Employee.query

    # Filter by position, department, and status (using IDs)
    if position_id:
        employees = employees.filter_by(position_id=position_id)
    if department_id:
        employees = employees.filter_by(department_id=department_id)
    if status_id:
        employees = employees.filter_by(status_id=status_id)

    # Fetch all filtered employees
    employee_list = employees.all()

    # Convert the list of employee objects to a list of dictionaries
    employee_data = []
    for employee in employee_list:
        actual_status = Status.query.get(employee.status_id).status_name
        actual_department = Department.query.get(employee.department_id).department_name
        actual_position = Position.query.get(employee.position_id).position_name
        actual_salary = Position.query.get(employee.position_id).salary
        employee_info = {
            "id": employee.id,
            "name": employee.name,
            "address": employee.address,
            "status_id": employee.status_id,
            "status": actual_status,
            "department_id": employee.department_id,
            "department": actual_department,
            "position_id": employee.position_id,
            "position": actual_position,
            "salary": actual_salary,
            "manager": employee.manager,
            "image": employee.image
        }
        # Append each employee's dictionary to the list
        employee_data.append(employee_info)

    # Return the list of employees as JSON
    return jsonify({"employees": employee_data}), 200