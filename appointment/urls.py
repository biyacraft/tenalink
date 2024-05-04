from django.urls import path
from appointment.views import *

app_name = 'appointment'
urlpatterns = [
    path('fill-date', fill_date, name="fill-date"),
    path('schedule-dtime', schedule_dtime, name="schedule"),
    path('fill-date-admin', fill_date_admin, name="fill-date-admin"),
    path('schedule-dtime_admin', schedule_dtime_admin, name="schedule-admin"),
    path('view-cv/<str:id>', view_cv, name="view-cv"),
    path('approve-doctor/<str:id>', approve_doctor, name="approve-doctor"),
    path('test', test, name="test"),
    path('change_status/<str:id>/<str:option>/<str:purpose>', change_status, name="change_status"),
]