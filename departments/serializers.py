from rest_framework import serializers
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.IntegerField(source="employees.count", read_only=True)

    class Meta:
        model = Department
        fields = ["id", "department_name", "location", "employee_count"]
