from .models import Department

def list_departments():
    return Department.objects.all()

def get_department_by_id(department_id):
    return Department.objects.get(pk=department_id)

def create_department(department_name: str, location: str) -> Department:
    return Department.objects.create(
        department_name=department_name.strip(),
        location=location.strip()
    )

def update_department(department: Department, department_name: str, location: str) -> Department:
    department.department_name = department_name.strip()
    department.location = location.strip()
    department.save()
    return department

def delete_department(department: Department):
    department.delete()
