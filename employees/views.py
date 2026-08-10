from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Employee
from .serializers import EmployeeSerializer
from .filters import EmployeeFilter
from employees.services import get_dashboard_stats

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("department").all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    search_fields = ["employee_name", "email"]
    ordering_fields = ["salary", "experience", "employee_name"]

class DashboardAPIView(APIView):
    def get(self, request):
        stats = get_dashboard_stats()
        return Response(stats)
