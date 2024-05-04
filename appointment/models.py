from django.db import models
from account.models import Patient, Doctor
from datetime import datetime
from datetime import timedelta


class AppDay(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    schedule = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date) + " " + self.patient.email + " " + self.schedule


class AppAdmin(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, unique=True)
    schedule = models.ForeignKey(AppDay, on_delete=models.SET_NULL, null=True)
    room_id = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(default=1)

    host = models.BooleanField(default=False)
    attendee = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    @property
    def left_time(self):
        start, endzone = self.schedule.schedule.split('-')
        end, zone = endzone.split()
        dt = self.schedule.date

        hr = int(start.split(':')[0])
        if zone == "Night":
            if hr >= 7:
                hr -= 6
            else:
                hr += 18
        else:
            hr += 6
        if hr == 24: hr -= 1

        b = datetime(dt.year, dt.month, dt.day, hr)
        c = datetime.now()
        e = b - c
        return e

    @property
    def get_status(self):
        tm = self.left_time
        day = tm.days
        sec = tm.seconds
        hour = sec // 3600
        if self.status == 0:
            return 0
        if day < 0:
            if day == -1 and hour == 23:
                return 1
            return 3
        return 2

    def __str__(self):
        return self.patient.first_name + ' ' + self.doctor.first_name


class WorkingDay(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, blank=True, null=True)
    schedule = models.CharField(max_length=200, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date) + " " + self.doctor.email + " " + self.schedule


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    schedule = models.ForeignKey(WorkingDay, on_delete=models.SET_NULL, null=True)
    room_id = models.CharField(max_length=20, blank=True, null=True)
    status = models.IntegerField(default=1)

    host = models.BooleanField(default=False)
    attendee = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    @property
    def left_time(self):
        start, endzone = self.schedule.schedule.split('-')
        end, zone = endzone.split()
        dt = self.schedule.date

        hr = int(start.split(':')[0])
        if zone.lower() == "night":
            if hr >= 7:
                hr -= 6
            else:
                hr += 18
        else:
            hr += 6
        if hr == 24: hr -= 1

        b = datetime(dt.year, dt.month, dt.day, hr)
        c = datetime.now()
        e = b - c
        return e

    @property
    def get_status(self):
        tm = self.left_time
        day = tm.days
        sec = tm.seconds
        hour = sec // 3600
        if self.status == 0:
            return 0
        if day < 0:
            if day == -1 and hour == 23:
                return 1
            return 3
        return 2

    def __str__(self):
        return self.patient.first_name + ' ' + self.doctor.first_name
