from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('partials/stats/', views.dashboard_stats_partial, name='dashboard-stats-partial'),
    
    path('employees/', views.employee_list_view, name='employee-list'),
    path('employees/table/', views.employee_table_partial, name='employee-table-partial'),
    path('employees/form/', views.employee_form_partial, name='employee-create-form'),
    path('employees/form/<int:employee_id>/', views.employee_form_partial, name='employee-edit-form'),
    path('employees/<int:employee_id>/delete/', views.employee_delete_view, name='employee-delete'),

    path('departments/', views.department_list_view, name='department-list'),
    path('departments/table/', views.department_table_partial, name='department-table-partial'),
    path('departments/form/', views.department_form_partial, name='department-create-form'),
    path('departments/form/<int:department_id>/', views.department_form_partial, name='department-edit-form'),
    path('departments/<int:department_id>/delete/', views.department_delete_view, name='department-delete'),
]
