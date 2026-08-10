import pytest
from departments.models import Department
from employees.models import Employee

@pytest.fixture
def sample_department(db):
    return Department.objects.create(department_name="Engineering", location="Building A")

@pytest.fixture
def sample_employee(db, sample_department):
    return Employee.objects.create(
        employee_name="Alice Vance",
        email="alice@example.com",
        salary=85000.00,
        experience=5,
        department=sample_department
    )
