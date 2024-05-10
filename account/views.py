from django.shortcuts import render, redirect
from account.forms import *
from django.contrib import messages
from account.decorators import *
from django.http import QueryDict
from django.urls import reverse
from account.include import *
from account.models import Patient, Doctor

qd = QueryDict("", mutable=True)


def home_page(request):
    return render(request, "recommendation/index.html")


def login(request):
    fg = 'admin'
    rvk = request.GET.get("revoke")

    if request.method == "POST":
        if request.POST.get('email_field') is not None:
            em = request.POST.get('email')
            if Revoke.objects.filter(patient__email=em).exists() or Revoke.objects.filter(doctor__email=em).exists():
                messages.error(request, "Already password revoke is requested check your email.")
                qd = QueryDict("", mutable=True)
                us = "patient"
                if Doctor.objects.filter(email=em).exists():
                    us = "doctor"
                qd.update({"revoke": "code", "email": em, 'user': us})
                return redirect(reverse('account:login') + f'?{qd.urlencode()}')
            else:
                try:
                    us = "patient"
                    if Doctor.objects.filter(email=em).exists():
                        us = "doctor"
                        rv = Revoke.objects.create(doctor=Doctor.objects.get(email=em))
                    else:
                        rv = Revoke.objects.create(patient=Patient.objects.get(email=em))
                    EmailThread('email/password_reset.html', em, {'name': em, 'otp_code': rv.code}).start()
                    qd = QueryDict("", mutable=True)
                    qd.update({"revoke": "code", "email": em, 'user': us})
                    messages.success(request, "We have sent a message to your email.")
                    return redirect(reverse('account:login') + f'?{qd.urlencode()}')
                except:
                    messages.error(request, "Your email doesn't Exist in our database.")
        elif request.POST.get('code') is not None:
            em = request.GET.get('email')
            cd = request.POST.get('codechar')
            rl = request.GET.get('user')
            try:
                if rl == "patient":
                    rv = Revoke.objects.get(patient__email=em)
                else:
                    rv = Revoke.objects.get(doctor__email=em)
                if cd == rv.code:
                    messages.success(request, "Good Job please update your password.")
                    qd = QueryDict("", mutable=True)
                    qd.update(
                        {"revoke": "password", "id": rv.patient.id if rl == "patient" else rv.doctor.id, 'user': rl})

                    rv.delete()
                    return redirect(reverse('account:login') + f'?{qd.urlencode()}')
                else:
                    messages.error(request, "The Code you have entered isn't correct.")
            except:
                messages.error(request, "Your email doesn't Exist in our database.")
        elif request.POST.get('login') is not None:
            email = request.POST.get('email')
            password = request.POST.get('password')
            is_doctor = request.POST.get('is_doctor')

            flag = ""

            if is_doctor is None:
                if Patient.objects.filter(email=email, password=password).exists():
                    user = Patient.objects.get(email=email, password=password)
                    if user.is_admin:
                        flag = "admin"
                    else:
                        flag = "patient"
                    request.session["user-role"] = flag
                    request.session["email"] = user.email
                    messages.success(request, "Successfully logged in to system. welcome!")
                    return redirect(f'dashboard:{flag}-dashboard')
                else:
                    messages.warning(request, "User doesn't exist!, with this credentials.")
            else:
                if Doctor.objects.filter(email=email, password=password).exists():
                    user = Doctor.objects.get(email=email, password=password)
                    request.session["user-role"] = 'doctor'
                    request.session["email"] = user.email
                    messages.success(request, "Successfully logged in to system as a Dr. welcome!")
                    return redirect(f'dashboard:doctor-dashboard')
                else:
                    messages.warning(request, "User doesn't exist!, with this credentials.")
    context = {
        'id': request.GET.get("id"),
        'reset_req': request.GET.get("user"),
        'role': fg,
        'revoke': rvk,
    }
    return render(request, "tenassist/login.html", context)


def forgot_password(request):
    itm = request.GET.get('revoke')
    qd = QueryDict("", mutable=True)
    value = "true"
    if itm == 'true':
        value = "email"
    elif itm == "email":
        value = "code"
    qd.update({"revoke": value})
    return redirect(reverse('account:login') + f'?{qd.urlencode()}')


def update_password_forgot(request, pk, role):
    qd = QueryDict("", mutable=True)
    if request.method == "POST":
        np = request.POST.get('new_password')
        rnp = request.POST.get('renew_password')
        if np != rnp:
            messages.warning(request, "Two password aren't match..")
            qd.update({'revoke': 'password', "id": pk, 'user': role})
        else:
            if role == 'patient':
                Patient.objects.filter(id=pk).update(password=np)
            else:
                Doctor.objects.filter(id=pk).update(password=np)
            messages.success(request, "Your password are successfully updated!")
    return redirect(reverse(f'account:login') + f'?{qd.urlencode()}')


def update_password(request, pk, role):
    cp = request.POST.get('current_password')
    np = request.POST.get('new_password')
    rnp = request.POST.get('renew_password')
    print(cp, np, rnp)
    if request.method == "POST":
        cp = request.POST.get('current_password')
        np = request.POST.get('new_password')
        rnp = request.POST.get('renew_password')
        if np != rnp:
            messages.warning(request, "Your new and re-enter password aren't much.")
        else:

            if role == "doctor":
                us = Doctor.objects.get(id=pk)
            else:
                us = Patient.objects.get(id=pk)
            if us.password != cp:
                messages.warning(request, "Your new and old password aren't much.")
            else:
                us.password = np
                us.save()
                messages.success(request, "Your password are successfully updated!")
    qd.update({'pages': 'profile'})
    flag = user_role(request)
    return redirect(reverse(f'dashboard:{flag}-dashboard') + f'?pages=profile')


@login_first
def logout(request):
    request.session.pop("user-role", 0)
    request.session.pop("email", 0)
    return redirect('account:login')


def register_patient(request, _to):
    form = PatientRegistrationForm()
    is_patient = True
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            messages.success(request, "Welcome, you are successfully registered.")
            if _to == 'admin':
                instance.is_admin = True
            else:
                instance.is_patient = True
            instance.save()

            if _to == 'index':
                return redirect('account:login')

            qd.update({'pages': f'{_to}s'})
            return redirect(reverse('dashboard:admin-dashboard') + f'?{qd.urlencode()}')
        else:
            messages.error(request, "Not Valid Form, please fill form accordingly or may account exist.")
    if _to == 'index':
        return render(request, 'tenassist/register_patient.html', {'patient_form': form})
    qd.clear()
    qd.update({'pages': f'register_{_to}'})
    return redirect(reverse('dashboard:admin-dashboard') + f'?{qd.urlencode()}')


def register_doctor(request, _from):
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Welcome, you are successfully registered.")
            if _from == 'index':
                return redirect('account:login')
            qd.update({'pages': 'doctors_waiting'})
            return redirect(reverse('dashboard:admin-dashboard') + f'?{qd.urlencode()}')
        else:
            messages.error(request, "Not Valid Form, please fill form accordingly or may account exist.")
    if _from == 'index':
        return render(request, 'tenassist/register_doctor.html', {'doctor_form': DoctorRegistrationForm()})
    qd.clear()
    qd.update({'pages': 'register_doctor'})
    return redirect(reverse('dashboard:admin-dashboard') + f'?{qd.urlencode()}')


def delete_user(request, pk, role):
    print('notifies', pk, role)
    return redirect('dashboard:admin-dashboard')
