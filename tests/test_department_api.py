import pytest
from rest_framework import status
from departments.models import Department

@pytest.mark.django_db
def test_create_department(client):
    response = client.post("/api/v1/departments/", {
        "department_name": "Finance",
        "location": "Floor 3"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert Department.objects.filter(department_name="Finance").exists()

@pytest.mark.django_db
def test_delete_department_protected(client, sample_department, sample_employee):
    response = client.delete(f"/api/v1/departments/{sample_department.id}/")
    assert response.status_code == status.HTTP_409_CONFLICT
    assert Department.objects.filter(id=sample_department.id).exists()
