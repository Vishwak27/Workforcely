import django_filters
from .models import Employee

class EmployeeFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name="department__id")

    class Meta:
        model = Employee
        fields = ["department"]
