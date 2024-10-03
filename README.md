# Employee Management System

## Project Overview

This is a CRUD-based Employee Management System built with Flask, SQLite for development, and Docker for containerization and deployment. The application allows the management of employees, departments, positions, and statuses through a RESTful API. User authentication is implemented using Flask-Login.

## Features

- **CRUD Operations**:
  - Employees: Create, read, update, delete employees.
  - Positions: Manage job positions, including salary details.
  - Departments: Manage departments and assign managers.
  - Statuses: Track employee status (e.g., active, probation, resigned).
  
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
- Docker and Docker Compose

### Local Development Setup

1. **Clone the Repository**:
   ```bash
   git clone <your-repository-url>
   cd employee-management
