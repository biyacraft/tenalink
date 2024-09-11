from django.db import models
import random
from django.utils.crypto import get_random_string


class Patient(models.Model):
    first_name = models.CharField(max_length=100, )
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='patient_photo', blank=True, default='user_avatar.png')

    is_admin = models.BooleanField(max_length=5, default=False)
    is_patient = models.BooleanField(max_length=5, default=False)

    def __str__(self):
        return self.first_name


class Doctor(models.Model):
    SPECIALITY_CHOICES = [
        ('Dermatologist', 'Dermatologist'),
        ('Dentist', 'Dentist'),
        ('Sexologist', 'Sexologist'),
        ('Dietitian/Nutritionist', 'Dietitian/Nutritionist'),
        ('General Physician', 'General Physician'),
        ('Orthopedist', 'Orthopedist'),
        ('Gynecologist', 'Gynecologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Psychologist', 'Psychologist'),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    specialization = models.CharField(max_length=100, choices=SPECIALITY_CHOICES)
    document = models.FileField(upload_to='doctor_document')
    photo = models.ImageField(upload_to='doctor_photo', blank=True, default='user_avatar.png')
    is_verified = models.BooleanField(default=True)

    degree = models.CharField(max_length=100, null=True, blank=True)
    experience = models.CharField(max_length=100, default='0')
    about = models.TextField(max_length=500, null=True, blank=True)
    fee = models.IntegerField(default=0)
    hospital = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Revoke(models.Model):
    code = models.CharField(max_length=6, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()

        super().save(*args, **kwargs)

    def generate_unique_code(self):
        code = "".join([str(random.randint(0, 9)) for i in range(6)])
        while Revoke.objects.filter(code=code).exists():
            code = "".join([str(random.randint(0, 9)) for i in range(6)])
        return code

    def __str__(self):
        return self.code
