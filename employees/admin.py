from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "employee_name", "email", "salary", "experience", "department")
    list_filter = ("department",)
    search_fields = ("employee_name", "email")
