from django.urls import path
from dashboard.views import *

app_name = "dashboard"
urlpatterns = [
    path('admin/', admin_dashboard, name="admin-dashboard"),
    path('patient/', patient_dashboard, name="patient-dashboard"),
    path('doctor/', doctor_dashboard, name="doctor-dashboard"),
    path('delete/<str:pk>/<str:identity>/', delete, name="delete-item"),
    path('deactivate/<str:id>/', deactivate, name="deactivate"),
]
