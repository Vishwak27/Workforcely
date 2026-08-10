from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from departments.models import Department

class Employee(models.Model):
    employee_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    salary = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    experience = models.IntegerField(validators=[MinValueValidator(0)])
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="employees"
    )

    class Meta:
        ordering = ["-salary"]

    def __str__(self):
        return f"{self.employee_name} ({self.department.department_name})"
