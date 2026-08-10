from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db.models import ProtectedError

from departments.services import (
    list_departments,
    get_department_by_id,
    create_department,
    update_department,
    delete_department,
)
from departments.models import Department
from employees.services import (
    get_filtered_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee,
    get_dashboard_stats,
)
from employees.models import Employee


# Dashboard
def dashboard_view(request):
    return render(request, "dashboard.html")

def dashboard_stats_partial(request):
    stats = get_dashboard_stats()
    return render(request, "_stats_partial.html", stats)


# Employees
def employee_list_view(request):
    departments = list_departments()
    return render(request, "employees/list.html", {"departments": departments})

def employee_table_partial(request):
    department_id = request.GET.get("department")
    search_query = request.GET.get("search")
    ordering = request.GET.get("ordering", "-salary")
    page_number = request.GET.get("page", 1)

    employees_qs = get_filtered_employees(
        department_id=department_id,
        search_query=search_query,
        ordering=ordering
    )

    paginator = Paginator(employees_qs, 10)
    page_obj = paginator.get_page(page_number)
    departments = list_departments()

    context = {
        "page_obj": page_obj,
        "departments": departments,
        "selected_department": int(department_id) if department_id and department_id.isdigit() else "",
        "search_query": search_query or "",
        "ordering": ordering,
    }
    return render(request, "employees/_table.html", context)

def employee_form_partial(request, employee_id=None):
    departments = list_departments()
    employee = None
    if employee_id:
        employee = get_employee_by_id(employee_id)

    errors = {}
    if request.method == "POST":
        name = request.POST.get("employee_name", "").strip()
        email = request.POST.get("email", "").strip()
        salary_str = request.POST.get("salary", "0")
        exp_str = request.POST.get("experience", "0")
        dept_id = request.POST.get("department")

        try:
            salary = Decimal(salary_str)
            if salary <= 0:
                errors["salary"] = "Salary must be greater than zero."
        except Exception:
            errors["salary"] = "Invalid salary amount."

        if not name:
            errors["employee_name"] = "Name is required."
        if not email:
            errors["email"] = "Email is required."
        if not dept_id:
            errors["department"] = "Department is required."

        if not errors:
            try:
                if employee:
                    update_employee(employee, name, email, salary, int(exp_str), int(dept_id))
                else:
                    create_employee(name, email, salary, int(exp_str), int(dept_id))

                response = HttpResponse(status=204)
                response["HX-Trigger"] = "employeeChanged"
                return response
            except Exception as e:
                errors["non_field"] = str(e)

    context = {
        "employee": employee,
        "departments": departments,
        "errors": errors,
    }
    return render(request, "employees/_form.html", context)

def employee_delete_view(request, employee_id):
    if request.method == "DELETE":
        employee = get_object_or_404(Employee, pk=employee_id)
        delete_employee(employee)
        return HttpResponse("")


# Departments
def department_list_view(request):
    return render(request, "departments/list.html")

def department_table_partial(request):
    departments = list_departments()
    return render(request, "departments/_table.html", {"departments": departments})

def department_form_partial(request, department_id=None):
    dept = None
    if department_id:
        dept = get_department_by_id(department_id)

    errors = {}
    if request.method == "POST":
        name = request.POST.get("department_name", "").strip()
        location = request.POST.get("location", "").strip()

        if not name:
            errors["department_name"] = "Department name is required."
        if not location:
            errors["location"] = "Location is required."

        if not errors:
            try:
                if dept:
                    update_department(dept, name, location)
                else:
                    create_department(name, location)

                response = HttpResponse(status=204)
                response["HX-Trigger"] = "departmentChanged"
                return response
            except Exception as e:
                errors["non_field"] = str(e)

    return render(request, "departments/_form.html", {"department": dept, "errors": errors})

def department_delete_view(request, department_id):
    if request.method == "DELETE":
        dept = get_object_or_404(Department, pk=department_id)
        try:
            delete_department(dept)
            return HttpResponse("")
        except ProtectedError:
            return HttpResponse(
                '<div class="p-3 mb-4 text-sm font-medium text-red-800 bg-red-100 rounded-lg">Cannot delete department with active employees.</div>',
                status=409,
                headers={"HX-Retarget": "#toast-container"}
            )
