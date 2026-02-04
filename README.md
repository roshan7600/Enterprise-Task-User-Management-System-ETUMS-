🚀 Enterprise Task & User Management System (ETUMS)

A production-ready backend system built with Django & Django REST Framework, implementing JWT authentication, role-based access control, secure APIs, bulk data handling, logging, and API documentation.

This project reflects real-world backend engineering practices used in enterprise applications.

🧩 Features Overview
🔐 Authentication & Authorization

JWT-based authentication (Access & Refresh tokens)

Role-Based Access Control (RBAC)

Role	                                Capabilities
-------------                      ----------------------------
ADMIN                             Full system access, user management (via admin panel), task oversight    

MANAGER                           Create & assign tasks, track progress

EMPLOYEE                          View assigned tasks, update task status only

Secure permission handling per API action

📋 Task Management

Create, update, delete tasks

Assign tasks to employees

Task status tracking:

TODO

IN_PROGRESS

DONE

Employees can update only task status

Managers/Admins can view and manage all relevant tasks

⚡ Performance & Scalability

Pagination for large datasets

Optimized queries using select_related

Bulk task creation (JSON)

Bulk task upload via CSV

Transaction-safe operations

🔒 API Security

Request throttling (rate limiting)

Secure HTTP headers

Permission-based API access

Protection against brute-force attacks

🧾 Logging & Monitoring

Centralized Python logging

Logs stored in file (logs/app.log)

API failures and authentication errors tracked

Production-style observability

📘 API Documentation

Swagger / OpenAPI documentation

JWT authentication supported inside Swagger UI

Interactive API testing

🧪 Testing

Unit testing (DRF APITestCase)

API testing via Postman & Swagger

Query performance verification

🏗️ Tech Stack

Backend: Django, Django REST Framework

Database: MySQL

Authentication: JWT (SimpleJWT)

Documentation: Swagger (drf-spectacular)

Logging: Python logging

Tools: Postman, Django Admin

🧠 User Roles & Responsibilities
👑 Admin

Create and manage users via Django Admin

View and manage all tasks

Full system access

🧑‍💼 Manager

Create tasks

Assign tasks to employees

Track task progress

👨‍💻 Employee

View assigned tasks only

Update task status (no other changes)

📂 Project Structure
Enterprise Task & User Management System/
│
├── etums/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── tasks/
│   └── core/
│
├── logs/
│   └── app.log
│
├── manage.py
├── requirements.txt
└── venv/

🔑 API Endpoints (Sample)

Authentication
POST /api/auth/login/
POST /api/auth/refresh/

Tasks
GET    /api/tasks/
POST   /api/tasks/
PATCH  /api/tasks/{id}/
DELETE /api/tasks/{id}/
POST   /api/tasks/bulk-create/
POST   /api/tasks/bulk-upload/

📊 Swagger API Docs

After running the server:

http://127.0.0.1:8000/api/docs/

▶️ How to Run the Project
# Activate virtual environment
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

🧪 Run Tests
python manage.py test

🎯 Why This Project Matters

This project demonstrates:

Real-world backend architecture

Secure API design

Role-based access control

Performance optimization

Enterprise-level coding practices

It is resume-worthy, interview-ready, and production-oriented.

📌 Interview Talking Points

“Built a role-based backend system using Django & DRF.”

“Implemented JWT authentication with secure API permissions.”

“Handled bulk data efficiently using transactions and batch inserts.”

“Optimized database queries and added logging for monitoring.”

“Documented APIs using Swagger (OpenAPI).”

🏁 Status

✅ Project Completed
✅ Production Ready
✅ Interview Ready
