from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, DashboardAPIView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('dashboard/', DashboardAPIView.as_view(), name='api-dashboard'),
] + router.urls
