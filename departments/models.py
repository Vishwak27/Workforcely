from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)

    class Meta:
        ordering = ["department_name"]

    def __str__(self):
        return self.department_name
