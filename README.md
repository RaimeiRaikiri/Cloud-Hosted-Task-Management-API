# Cloud-Hosted-Task-Management-API

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![CI](https://github.com/RaimeiRaikiri/Cloud-Hosted-Task-Management-API/actions/workflows/ci.yaml/badge.svg)

## Live Demo

API Documentation:
https://cloud-hosted-task-management-api.onrender.com/docs

## Overview

A RESTful task management API built with FastAPI and PostgreSQL. The application supports user registration, authentication using JWT's, and CRUD operations for managing tasks.

The project demonstrates modern backend developement practices including containerisation, automated testing, continuous integration, and cloud deployment.

### Features

- User registration and authentication
- JWT-based authorization
- Create, read, update, and delete tasks
- PostgreSQL database integration
- SQLAlchemy ORM
- Automated testing with Pytest
- Code quality checks with Ruff
- Docker containerisation
- GitHub Actions CI pipeline
- Cloud deployment on Render
- Interactive API documentation via Swagger/OpenAPI

## Tech Stack

| Category         | Technology     |
| ---------------- | -------------- |
| Language         | Python 3.12    |
| Framework        | FastAPI        |
| Database         | PostgreSQL     |
| ORM              | SQLAlchemy     |
| Authentication   | JWT            |
| Testing          | Pytest         |
| Linting          | Ruff           |
| Containerisation | Docker         |
| CI               | GitHub Actions |
| Deployment       | Render         |

## Architecture

![App Architecture](screenshots/architecture.png)

## API Documentation

![Swagger UI](screenshots/swagger-docs.png)

Interactive Swagger documentation is available at:
https://cloud-hosted-task-management-api.onrender.com/docs

## Running Locally

### Clone the repository

```
git clone https://github.com/RaimeiRaikiri/Cloud-Hosted-Task-Management-API.git
cd Cloud-Hosted-Task-Management-API
```

### Create a virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```

### Configure environment variables

Create a .env file:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/taskdb
SECRET_KEY=your-secret-key
```

### Start the application

uvicorn app.main:app --reload

## Running wih Docker

Build and start the application:

```
docker compose up --build
```

The API will be available at:

```
http://localhost:8000/docs
```

## Testing

Run the test suite:

```
pytest -v
```

Run tests with coverage:

```
pytest -v --cov=app --cov-report=term
```

## Continuous Integration

GitHub Actions automatically:

- Runs Ruff linting checks
- Executes the Pytest test suite
- Validates code quality before deployment

![GitHub Actions](screenshots/ci-passing.png)

## Why this project?

This project was developed to demonstrate practical backend engineering skills including REST API development, authentication, database design, testing, containerisation, CI workflows, and cloud deployment.
