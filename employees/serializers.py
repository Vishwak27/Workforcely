from rest_framework import serializers
from .models import Employee
from departments.models import Department

class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.department_name", read_only=True)

    class Meta:
        model = Employee
        fields = ["id", "employee_name", "email", "salary", "experience", "department", "department_name"]

    def validate_salary(self, value):
        if value <= 0:
            raise serializers.ValidationError("Salary must be greater than zero.")
        return value
