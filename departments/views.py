from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import ProtectedError
from .models import Department
from .serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ["department_name", "location"]
    ordering_fields = ["department_name", "location"]

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete department while employees belong to it."},
                status=status.HTTP_409_CONFLICT
            )
