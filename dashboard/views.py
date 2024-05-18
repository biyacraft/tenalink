from django.shortcuts import render, redirect, reverse
from account.models import *
from dashboard.models import *
from appointment.models import *
from django.contrib import messages
from account.forms import *
from account.decorators import *
from account.include import user_info, user_role as u_role, automate_email
from account.forms import PatientRegistrationForm, DoctorRegistrationForm

from datetime import date as dt


@login_first
def delete(request, pk, identity):
    page = request.GET.get('pages', '')

    if identity == "patient":
        try:
            print(page)
            patient = Patient.objects.get(id=pk)
            patient.delete()
            messages.success(request, "Patient deleted successfully.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
        except:
            messages.error(request, "Sorry, we can't delete patient.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
    elif identity == "doctor":
        try:
            doctor = Doctor.objects.get(id=pk)
            doctor.delete()
            messages.success(request, "Doctor deleted successfully.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
        except:
            messages.error(request, "Sorry, we can't delete doctor.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
    elif identity == "admin":
        try:
            patient = Patient.objects.get(id=pk)
            patient.save()
            messages.success(request, "Admin removed successfully.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
        except:
            messages.error(request, "Sorry, we can't remove admin.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
    elif identity == "feedback":
        try:
            feedback = Feedback.objects.get(id=pk)
            feedback.delete()
            messages.success(request, "Feedback deleted successfully.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=view_feedback")
        except:
            messages.error(request, "Sorry, we can't delete feedback.")
            return redirect(reverse('dashboard:admin-dashboard') + "?pages=view_feedback")
    elif identity == "appointment":
        try:
            appointment = Appointment.objects.get(id=pk)
            appointment.delete()
            messages.success(request, "Appointment deleted successfully.")
            return redirect('dashboard:patient-dashboard')
        except:
            messages.error(request, "Sorry, we can't delete appointment.")
            return redirect('dashboard:patient-dashboard')
    elif identity == "prescription":
        try:
            prescription = Prescription.objects.get(id=pk)
            prescription.delete()
            messages.success(request, "Prescription deleted successfully.")
            return redirect('dashboard:patient-dashboard')
        except:
            messages.error(request, "Sorry, we can't delete prescription.")
            return redirect('dashboard:patient-dashboard')
    elif identity == "medical_history":
        try:
            medical_history = MedicalHistory.objects.get(id=pk)
            medical_history.delete()
            messages.success(request, "Medical history deleted successfully.")
            return redirect('dashboard:patient-dashboard')
        except:
            messages.error(request, "Sorry, we can't delete medical history.")
            return redirect('dashboard:patient-dashboard')
    elif identity == "working_day":
        try:
            working_day = WorkingDay.objects.get(id=pk)
            working_day.delete()
            messages.success(request, "Working day deleted successfully.")
            return redirect(reverse('dashboard:doctor-dashboard') + "?pages=remove_day")
        except:
            messages.error(request, "Sorry, we can't delete working day.")
            return redirect(reverse('dashboard:doctor-dashboard') + "?pages=remove_day")


@login_first
def deactivate(request, id):
    page = request.GET.get('pages', '')
    try:
        dr = Doctor.objects.get(id=id)
        dr.is_verified = False
        dr.save()
        messages.success(request, "Doctor deactivated successfully.")
        return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)
    except:
        messages.error(request, "Sorry, we can't deactivate Doctor.")
        return redirect(reverse('dashboard:admin-dashboard') + "?pages=" + page)


@login_first
@admin_only
def admin_dashboard(request):
    page = request.GET.get('pages')
    user = user_info(request)
    purpose = request.GET.get('purpose')
    app_id = request.GET.get('app_id')
    user_role = u_role(request)

    if request.method == "POST":
        if request.POST.get('update') is not None:
            update_form = PatientRegistrationForm(request.POST, request.FILES, instance=user)
            if update_form.is_valid():
                request.session["email"] = request.POST.get('email')
                update_form.save()
                messages.success(request, "Thank you, for updating your profile.")
            else:
                messages.error(request, "Sorry, we can't update your profile.")

    if request.GET.get('decline') is not None:
        try:
            app_id = request.GET.get('decline')
            app = AppAdmin.objects.get(id=app_id)
            app.delete()
            messages.success(request, "Appointment declined successfully.")
        except:
            messages.error(request, "Sorry, we can't decline appointment.")
        return redirect(reverse('dashboard:admin-dashboard') + "?pages=doctors_waiting")
    query = AppAdmin.objects.filter(patient=user)
    context = {
        'page': page,
        'user': user,
        'user_role': user_role,
        'app_id': app_id,
        'purpose': purpose,
        'update_form': PatientRegistrationForm(instance=user),
        'patients': Patient.objects.all(),
        'doctors': Doctor.objects.all(),
        'histories': sorted(query, key=lambda obj: obj.get_status),
        'admins': Patient.objects.filter(is_admin=True),
        'feedbacks': Feedback.objects.all(),
        'patient_form': PatientRegistrationForm(),
        'doctor_form': DoctorRegistrationForm(),
    }
    automate_email(request)
    return render(request, 'tenalink/admin-page.html', context)


@login_first
@patient_only
def patient_dashboard(request):
    page = request.GET.get('pages')
    user = user_info(request)
    app_id = request.GET.get('app_id')
    purpose = request.GET.get('purpose')
    user_role = u_role(request)

    unique_dates = []
    list_schedule = []
    doctors = Doctor.objects.filter(is_verified=True)

    if request.method == "POST":
        if request.POST.get('update') is not None:
            update_form = PatientRegistrationForm(request.POST, request.FILES, instance=user)
            if update_form.is_valid():
                request.session["email"] = request.POST.get('email')
                update_form.save()
                messages.success(request, "Thank you, for updating your profile.")
            else:
                messages.error(request, "Sorry, we can't update your profile.")
        if request.POST.get('feedback') is not None:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            fd = Feedback(user=user, name=name, email=email, subject=subject, body=message)
            try:
                fd.save()
                messages.success(request, "Thank you, we value your feedback.")
            except:
                messages.error(request, "Sorry, we can't add your feedback.")
        if request.POST.get('search') is not None:
            min_price = request.POST.get('min_price')
            max_price = request.POST.get('max_price')
            specialization = request.POST.getlist('specialization')[0]

            if min_price:
                doctors = doctors.filter(fee__gt=min_price)
            if max_price:
                doctors = doctors.filter(fee__lt=max_price)
            if specialization:
                doctors = doctors.filter(specialization=specialization)
        if request.POST.get('rate_doctor') is not None:
            id = request.POST.get('email')
            comment = request.POST.get('comment')
            rate = request.POST.get('range')
            try:
                doc = Doctor.objects.get(id=id)
                rt = Rate(doctor=doc, user=user, rate=int(rate), comment=comment)
                rt.save()
                messages.success(request, "Thank you, for rating doctors.")
                return redirect('dashboard:patient-dashboard')
            except:
                messages.error(request, "Sorry, we can't add your rating.")
    if request.GET.get('list_date'):
        email = request.GET.get('doc_email')
        date = request.GET.get('date')
        try:
            doctor = Doctor.objects.get(email=email, is_verified=True)
            list_schedule = WorkingDay.objects.filter(doctor=doctor, date__gte=dt.today()).filter(is_booked=False)
            if date != "":
                list_schedule = list_schedule.filter(date=date)

            for sch in list_schedule:
                if not sch.date in unique_dates:
                    unique_dates.append(sch.date)
        except:
            messages.error(request, "Sorry, we can't find any doctor or provide email.")
    query = Appointment.objects.filter(patient=user)
    context = {
        'page': page,
        'user': user,
        'user_role': user_role,
        'app_id': app_id,
        'purpose': purpose,
        'doctors': doctors,
        'update_form': PatientRegistrationForm(instance=user),
        'histories': sorted(query, key=lambda obj: obj.get_status),
        'prescriptions': Prescription.objects.filter(patient=user),
        'medical_histories': MedicalHistory.objects.filter(patient=user, is_shown=True),
        'book_info': {
            'dates': sorted(unique_dates)[:6],
            'schedules': list_schedule,
            'doc_email': request.GET.get('doc_email'),
        },
        'patient_form': PatientRegistrationForm(),
    }
    automate_email(request)
    return render(request, 'tenalink/patient-page.html', context)


@login_first
@doctor_only
def doctor_dashboard(request):
    page = request.GET.get('pages')
    app_id = request.GET.get('app_id')
    purpose = request.GET.get('purpose')
    user = user_info(request)
    user_role = u_role(request)
    rates = Rate.objects.filter(doctor=user)
    update_form = DoctorUpdateForm(instance=user)

    list_schedule = []
    unique_dates = []
    list_schedule_admin = []
    unique_dates_admin = []
    admin = user_info(request)

    if request.method == "POST":
        if request.POST.get('set_md_history') is not None:
            id = request.POST.get('id')
            is_shown = request.POST.get('is_shown')
            md_history = request.POST.get('md_history')
            if is_shown == "on":
                is_shown = False
            else:
                is_shown = True
            try:
                patient = Patient.objects.get(id=id)
                md = MedicalHistory(patient=patient, doctor=user, is_shown=is_shown, history=md_history)
                md.save()
                messages.success(request, "Thank you, for adding medical history.")
                return redirect('dashboard:doctor-dashboard')
            except:
                messages.error(request, "Sorry, we can't add your medical history.")
        if request.POST.get('set_prescription') is not None:
            id = request.POST.get('id')
            prescription = request.POST.get('prescription')
            try:
                patient = Patient.objects.get(id=id)
                pr = Prescription(patient=patient, doctor=user, prescription=prescription)
                pr.save()
                messages.success(request, "Thank you, for adding prescription.")
                return redirect('dashboard:doctor-dashboard')
            except:
                messages.error(request, "Sorry, we can't add your prescription.")
        if request.POST.get('update') is not None:
            update_form = DoctorUpdateForm(request.POST, request.FILES, instance=user)
            if update_form.is_valid():
                request.session["email"] = request.POST.get('email')
                update_form.save()
                messages.success(request, "Thank you, for updating your profile.")
            else:
                messages.error(request, "Sorry, we can't update your profile.")
    if request.GET.get('list_date_admin'):
        date = request.GET.get('date')
        admin_id = request.GET.get('admin')
        admin = Patient.objects.get(id=admin_id)
        try:
            list_schedule_admin = AppDay.objects.filter(patient=admin, date__gte=dt.today()).filter(is_booked=False)
            if date != "":
                list_schedule_admin = list_schedule_admin.filter(date=date)

            for sch in list_schedule_admin:
                if not sch.date in unique_dates_admin:
                    unique_dates_admin.append(sch.date)
        except:
            messages.error(request, "Sorry, we can't find any doctor or provide email.")
    if request.GET.get('list_date'):
        date = request.GET.get('date')
        try:
            list_schedule = WorkingDay.objects.filter(doctor=user).filter(is_booked=False)
            if date != "":
                list_schedule = list_schedule.filter(date=date)

            for sch in list_schedule:
                if not sch.date in unique_dates:
                    unique_dates.append(sch.date)
        except:
            messages.error(request, "Sorry, we can't find any doctor or provide email.")
    query = Appointment.objects.filter(doctor=user)
    admin_query = AppAdmin.objects.filter(doctor=user)
    context = {
        'page': page,
        'user': user,
        'purpose': purpose,
        'user_role': user_role,
        'app_id': app_id,
        'admins': Patient.objects.filter(is_admin=True),
        'histories': sorted(query, key=lambda obj: obj.get_status),
        'admin_histories': sorted(admin_query, key=lambda obj: obj.get_status),
        'rate_info': {
            'rates': rates,
            'total_rate': sum(obj.rate for obj in rates),
            'total_percent': ((sum(obj.rate for obj in rates) + 0.01) / ((10 * len(rates)) + 0.01)) * 100,
        },
        'book_info': {
            'dates': sorted(unique_dates)[:6],
            'schedules': list_schedule,
            'doc_email': user.email,
        },
        'book_info_admin': {
            'dates': sorted(unique_dates_admin)[:6],
            'schedules': list_schedule_admin,
            'add_email': admin.email,
        },
        'notifications': [
            a for a in Appointment.objects.filter(doctor=user) if
            (a.left_time.total_seconds() > 0) and (a.left_time.total_seconds() <= 1800)
        ],
        'doctor_form': DoctorRegistrationForm(),
        'update_form': update_form,
    }
    automate_email(request)
    return render(request, 'tenalink/doctor-page.html', context)
