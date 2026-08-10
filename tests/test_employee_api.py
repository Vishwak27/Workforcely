import pytest
from rest_framework import status
from employees.models import Employee

@pytest.mark.django_db
def test_create_employee_success(client, sample_department):
    payload = {
        "employee_name": "Bob Smith",
        "email": "bob@example.com",
        "salary": 65000.00,
        "experience": 3,
        "department": sample_department.id
    }
    response = client.post("/api/v1/employees/", payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["department_name"] == "Engineering"

@pytest.mark.django_db
def test_create_employee_invalid_salary(client, sample_department):
    payload = {
        "employee_name": "Charlie",
        "email": "charlie@example.com",
        "salary": -100.00,
        "experience": 2,
        "department": sample_department.id
    }
    response = client.post("/api/v1/employees/", payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "salary" in response.data

@pytest.mark.django_db
def test_filter_and_search_employees(client, sample_department):
    Employee.objects.create(employee_name="John Doe", email="john@test.com", salary=50000, experience=1, department=sample_department)
    Employee.objects.create(employee_name="Jane Roe", email="jane@test.com", salary=90000, experience=4, department=sample_department)

    response = client.get("/api/v1/employees/?search=John")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["employee_name"] == "John Doe"

@pytest.mark.django_db
def test_dashboard_api(client, sample_department, sample_employee):
    response = client.get("/api/v1/dashboard/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_employees"] == 1
    assert response.data["total_departments"] == 1
