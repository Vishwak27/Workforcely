# Employee & Department Management System (Workforcely)

A minimal, production-grade internal admin tool to manage Departments and Employees, built with **Django 5**, **Django REST Framework (DRF)**, **HTMX 1.9+**, and **Tailwind CSS**.

## Architecture & Design

- **Shared Service Layer**: Query logic, filters, validation, and aggregate counts reside exclusively in `departments/services.py` and `employees/services.py`. Both DRF ViewSets and HTMX template views consume these services.
- **Pure Python Web UI**: HTMX attributes (`hx-get`, `hx-post`, `hx-delete`, `hx-trigger`) drive async partial-page updates, eliminating JavaScript build tools or Node dependencies.
- **REST API & Swagger Docs**: Fully compliant OpenAPI 3.0 documentation served at `/api/schema/swagger-ui/`.

---

## Quick Setup & Execution

### 1. Prerequisites
- Python 3.11+

### 2. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Run migrations & load seed data
python manage.py migrate
python manage.py loaddata seed_data.json

# Start development server
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

## Running Automated Tests

```bash
pytest
```
