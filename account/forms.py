from django import forms
from .models import Patient, Doctor


class PatientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['is_admin', 'is_patient']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', "minlength": '4'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/yyyy'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': "image/*"}),
        }


class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'address', 'specialization', 'date_of_birth',
                  'document', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', "minlength": '4'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/yyyy'}),
            'document': forms.FileInput(attrs={'class': 'form-control', 'accept': "application/pdf"}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': "image/*"}),
        }


class AddInfoDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['degree', 'experience', 'about', 'fee', 'hospital', 'account_number']
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'about': forms.TextInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'hospital': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        exclude = ['is_verified']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', "minlength": '4'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'mm/dd/yyyy'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'about': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control', 'accept': "application/pdf"}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'hospital': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': "image/*"}),
        }
