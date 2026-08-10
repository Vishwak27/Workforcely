from django.contrib import admin
from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "department_name", "location")
    search_fields = ("department_name", "location")
