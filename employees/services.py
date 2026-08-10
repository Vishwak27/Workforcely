from decimal import Decimal
from django.db.models import Q
from departments.models import Department
from .models import Employee

def get_filtered_employees(department_id=None, search_query=None, ordering=None):
    queryset = Employee.objects.select_related("department").all()

    if department_id:
        queryset = queryset.filter(department_id=department_id)

    if search_query:
        query = search_query.strip()
        queryset = queryset.filter(
            Q(employee_name__icontains=query) | Q(email__icontains=query)
        )

    if ordering:
        allowed_ordering = ["salary", "-salary", "employee_name", "-employee_name", "experience", "-experience"]
        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

    return queryset

def get_employee_by_id(employee_id):
    return Employee.objects.select_related("department").get(pk=employee_id)

def create_employee(employee_name: str, email: str, salary: Decimal, experience: int, department_id: int) -> Employee:
    department = Department.objects.get(pk=department_id)
    return Employee.objects.create(
        employee_name=employee_name.strip(),
        email=email.strip().lower(),
        salary=Decimal(str(salary)),
        experience=int(experience),
        department=department
    )

def update_employee(employee: Employee, employee_name: str, email: str, salary: Decimal, experience: int, department_id: int) -> Employee:
    department = Department.objects.get(pk=department_id)
    employee.employee_name = employee_name.strip()
    employee.email = email.strip().lower()
    employee.salary = Decimal(str(salary))
    employee.experience = int(experience)
    employee.department = department
    employee.save()
    return employee

def delete_employee(employee: Employee):
    employee.delete()

def get_dashboard_stats():
    return {
        "total_employees": Employee.objects.count(),
        "total_departments": Department.objects.count(),
    }
