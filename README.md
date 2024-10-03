# Employee Management System

## Project Overview

This is a CRUD-based Employee Management System built with Flask, SQLite for development, and Docker for containerization and deployment. The application allows the management of employees, departments, positions, and statuses through a RESTful API. User authentication is implemented using Flask-Login.

## Features

- **CRUD Operations**:
  - Employees: Create, Read, Update, Delete employees.
  - Positions: Create, Read, Update, Delete positions.
  - Departments: Create, Read, Update, Delete departments.
  - Statuses: Create, Read, Update, Delete statuses.
  - User: Create (In case drop all table)
  
- **User Authentication**: 
  - Implemented using Flask-Login.
  
- **API Endpoints**:
  - Provides a RESTful API for interacting with employees, departments, positions, and statuses.
  
- **Input Validation**: 
  - Includes validation for employee names, addresses, salary, and image URLs.
  
- **Dockerized Application**:
  - The application is containerized with Docker and uses Docker Compose for running the application with PostgreSQL/MySQL for production.

## Technologies Used

- **Flask**: Backend framework
- **Flask-Login**: User authentication
- **SQLite**: Database for development
- **PostgreSQL/MySQL**: Database for production (with Docker)
- **Docker & Docker Compose**: Containerization for production-ready setup
- **Unit Testing**: `unittest` for automated testing

## Installation and Setup

### Prerequisites

- Python 3.10
- Docker and Docker Compose (Optional)

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/chaisupt/flask-employee-management.git
2. **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
3. **Install the Dependencies**:
    ```bash
    pip install -r requirements.txt
4. **Set Up Environment Variables: Create a `.env` file with the following content**:
    ```bash
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=sqlite:///employee_management.db
5. **Run the Application**:
    ```bash
    flask run
  - The application will run on `http://127.0.0.1:5000`

### Docker Setup

1. **Build Docker Image**:
    ```bash
    docker build -t flask-employee-management-app .
2. **Check Docker Image**:
    ```bash
    docker images
  - In `REPOSITORY` column should have `flask-employee-management-app`
3. **Run Docker Image**:
    ```bash
    docker run -P flask-employee-management-app
4. **Check port of the running container**:
    ```bash
    docker ps
  - The application will run on the front port that show in `PORTS` column before `->5000/tcp`

## Login/Logout Option

### Via Browser

#### Login method
- Visit `BASE_URL/login` on browser
- Simple login UI will popup

#### Logout method
- When logged in from UI the logout button will popup
- Visit `BASE_URL/logout`

### Via API endpoints

#### Login method
- Use `POST` method submit form-data to `BASE_URL/login`
  | KEY      | VALUE           |
  | -------- |:---------------:|
  | username | `YOUR_USERNAME` |
  | password | `YOUR_PASSWORD` |

#### Logout method
- Use `GET` or `POST` method to `BASE_URL/logout`

#### API Endpoints

 **HTTP Method** | **Endpoint**                          | **Description**                             | **Body**                        | **Body Parameter**                                                   
-----------------|---------------------------------------|---------------------------------------------|---------------------------------|----------------------------------------------------------------------
 POST            | /api/register                         | For register username and password to login | JSON                            | username, password                                                   
 GET             | /api/employee                         | Display List of Employee                    | -                               | -                                                                    
 POST            | /api/employee                         | Add new entry to Employee                   | JSON                            | name, address, status_id, department_id, position_id, manager, image 
 PATCH           | /api/employee/<employee_id>           | Update employee                             | JSON                            | name, address, status_id, department_id, position_id, manager, image 
 DELETE          | /api/employee/<employee_id>           | Mark employee status as "Delete"            | -                               | -                                                                    
 DELETE          | /api/employee/<employee_id>/permanent | Direct delete employee from database        | -                               | -                                                                    
 GET             | /api/status                           | Display List of Status                      | -                               | -                                                                    
 POST            | /api/status                           | Add new entry to Status                     | JSON                            | name                                                                 
 PATCH           | /api/status/<status_id>               | Update Status                               | JSON                            | name                                                                 
 DELETE          | /api/status/<status_id>               | Direct delete status from database          | -                               | -                                                                    
 GET             | /api/department                       | Display List of Department                  | -                               | -                                                                    
 POST            | /api/department                       | Add new entry to Department                 | JSON                            | name, manager_id(employee_id)                                        
 PATCH           | /api/department/<department_id>       | Update Department                           | JSON                            | name, manager_id(employee_id)                                        
 DELETE          | /api/department/<department_id>       | Direct delete department from database      | -                               | -                                                                    
 GET             | /api/position                         | Display List of Position                    | -                               | -                                                                    
 POST            | /api/position                         | Add new entry to Position                   | JSON                            | name, salary                                                         
 PATCH           | /api/position/<position_id>           | Update Position                             | JSON                            | name, salary                                                         
 DELETE          | /api/position/<position_id>           | Direct delete position from database        | -                               | -                                                                    
 Get             | /api/employees                        | Advanced Queries Filtering & Searching      | (Using Query Parameter Instead) | status_id, department_id, position_id                                



#### Example API Request (Using cURL)

To create a new position
  ```bash
  curl -X POST http://localhost:5000/api/position \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Backend Developer",
        "salary": 10000
    }'
  ```

#### Run Unit Test

Unit tests are written using unittest. You can run them with the following command:
  ```bash
  python -m unittest discover tests
  ```

#### Known Issues
- The application is currently configured to use SQLite for local development. Ensure that the database is switched to PostgreSQL/MySQL for production environments.

#### Future Improvements
- Implement soft deletion of employees instead of hard deletion.
- Add frontend components to interact with the API.
- Improve role-based access control for user permissions.

#### Credits
- Flask: https://flask.palletsprojects.com/
- Docker: https://www.docker.com/
- Flask-Login: https://flask-login.readthedocs.io/












