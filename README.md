# FastAPI Project – Complete Course Repository

A production‑ready project built with FastAPI, developed step‑by‑step through my free course on modern API development. This repository contains the full source code, architecture, and best practices demonstrated throughout the lessons.

👉 **Access the full free course here:**  
**https://tutorialibre.com/courses/programming-frameworks/fastapi/**

---

## 🚀 Project Overview

This repository showcases a complete backend application built with FastAPI, following real‑world patterns such as:

- Asynchronous programming with `async`/`await`
- Pydantic models for validation and serialization
- Dependency injection for clean architecture
- Router modularization
- Environment‑based configuration
- Database integration (SQLAlchemy or your chosen ORM)
- JWT authentication and authorization
- Docker deployment

The project is intentionally structured to teach maintainability, scalability, and production‑grade API design.

---

## 🧰 Features Implemented

- **User authentication** with JWT access tokens
- **CRUD operations** for core resources
- **Database migrations** (Alembic optional)
- **Async database access**
- **Error handling** with custom exceptions
- **CORS configuration** for frontend integration
- **Dockerized environment** for reproducible deployments

---

## 🛠️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/hochenri/fastapi-complete-course-project.git
cd fastapi-complete-course-project
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- Interactive docs: **http://localhost:8000/docs**
- Alternative docs: **http://localhost:8000/redoc**

---

## 📚 Learn FastAPI for Free

This project is part of my free course designed to teach:

- API fundamentals
- Clean architecture
- Real‑world backend development
- Deployment workflows
- Testing strategies

👉 **Start the course here:**  
**https://tutorialibre.com/courses/programming-frameworks/fastapi/**

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project or suggest new lessons.

---

## 📜 License

This project is released under the MIT License. You are free to use, modify, and distribute it.
