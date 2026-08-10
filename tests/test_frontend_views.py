import pytest
from rest_framework import status
from employees.models import Employee

@pytest.mark.django_db
def test_dashboard_page_render(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert b"System Dashboard" in response.content
    assert b'hx-headers=\'{"X-CSRFToken": "' in response.content

@pytest.mark.django_db
def test_employee_table_partial_filter(client, sample_department):
    Employee.objects.create(employee_name="Alice Smith", email="alice@test.com", salary=70000, experience=4, department=sample_department)
    Employee.objects.create(employee_name="Bob Brown", email="bob@test.com", salary=50000, experience=2, department=sample_department)

    response = client.get("/employees/table/?search=Alice")
    assert response.status_code == status.HTTP_200_OK
    assert b"Alice Smith" in response.content
    assert b"Bob Brown" not in response.content

@pytest.mark.django_db
def test_employee_delete_view(client, sample_employee):
    response = client.delete(f"/employees/{sample_employee.id}/delete/")
    assert response.status_code == status.HTTP_200_OK
    assert not Employee.objects.filter(id=sample_employee.id).exists()

@pytest.mark.django_db
def test_department_protected_delete_toast(client, sample_department, sample_employee):
    response = client.delete(f"/departments/{sample_department.id}/delete/")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert b"Cannot delete department with active employees." in response.content

@pytest.mark.django_db
def test_active_nav_tab_indicators(client):
    res_dash = client.get("/")
    assert b'border-b-2 border-accent bg-accent/10">Dashboard</a>' in res_dash.content

    res_emp = client.get("/employees/")
    assert b'border-b-2 border-accent bg-accent/10">Employees</a>' in res_emp.content

    res_dept = client.get("/departments/")
    assert b'border-b-2 border-accent bg-accent/10">Departments</a>' in res_dept.content
