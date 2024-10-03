from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(100), nullable=False)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'))
    manager = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(2000))  # store a image URL

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Function hash and set the password
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    # Function for check the password
    def check_password(self, password):
        return check_password_hash(self.password, password)