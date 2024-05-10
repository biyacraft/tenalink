import string
import random

from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, reverse, render
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from appointment.models import *
from account.include import user_info, EmailThread
from account.decorators import login_first

from account.models import Patient, Doctor


def test(request):
    des = EmailThread('email/appointment_reminder.html', "ayalkbettesfahun@gmail.com", {'name': 'Test-Name', 'otp_code': 8345}).start()
    print(des)
    return JsonResponse({'token': 'adfasd', 'uid': 'sdfs'}, safe=False)


def random_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@csrf_exempt
def change_status(request, id, option, purpose):
    try:
        test_patient = Patient.objects.first()
        test_doctor = Doctor.objects.first()
        if purpose == '0':
            app = AppAdmin.objects.get(id=id)
        else:
            app = Appointment.objects.get(id=id)

        if option == "in":
            if type(user_info(request)) == type(test_doctor):
                app.host = True
            else:
                app.attendee = True
            app.status = 0
        else:
            if type(user_info(request)) == type(test_doctor):
                app.host = False
            else:
                app.attendee = False
            if not (app.attendee and app.host):
                app.status = 1
        app.save()
        return JsonResponse({'response': "Data saved!"}, safe=False)
    except:
        return JsonResponse({'response': "Data not saved!"}, safe=False)


def date_spliter(date_list, spliter=60, ):
    night_schedule = []
    day_schedule = []

    for elm in date_list.split(','):
        if elm == "": continue
        tm, t = elm.split(':')
        st, end = tm.split('-')
        for rng in range(int(st), int(end)):
            if t == 'n' or t == 'N':
                if not rng in night_schedule:
                    night_schedule.append(rng)
            else:
                if not rng in day_schedule:
                    day_schedule.append(rng)

    return day_schedule, night_schedule


def add_schedule(due_date, time, doctor, from_admin=False):
    sch = "Day"
    for dt in time[0] + ["."] + time[1]:
        if dt == ".":
            sch = "Night"
            continue
        if from_admin:
            _ls = AppDay.objects.filter(patient=doctor, schedule__exact=f"{dt}:00-{dt + 1}:00 {sch}", date=due_date)
        else:
            _ls = WorkingDay.objects.filter(doctor=doctor, schedule__exact=f"{dt}:00-{dt + 1}:00 {sch}", date=due_date)

        if not _ls.exists():
            if from_admin:
                AppDay.objects.create(
                    patient=doctor,
                    schedule=f"{dt}:00-{dt + 1}:00 {sch}",
                    date=due_date
                )
            else:
                WorkingDay.objects.create(
                    doctor=doctor,
                    schedule=f"{dt}:00-{dt + 1}:00 {sch}",
                    date=due_date
                )


@login_first
def fill_date_admin(request):
    if request.POST.get('fill_date'):
        first_date = request.POST.get('date-first')
        last_date = request.POST.get('date-final')
        list_date = request.POST.get('date-input')

        try:
            rs = date_spliter(list_date)
        except:
            messages.error(request, "Sorry, Please follow free time input format.")
            return redirect(reverse('dashboard:admin-dashboard') + '?pages=add_app_day')
        y, m, d = first_date.split('-')

        email = user_info(request).email
        temp_doc = Patient.objects.get(email=email)

        if last_date == "":
            add_schedule(f"{y}-{m}-{d}", rs, temp_doc, from_admin=True)
        else:
            y2, m2, d2 = last_date.split('-')
            for rdt in range(int(d), int(d2) + 1):
                add_schedule(f"{y}-{m}-{rdt}", rs, temp_doc, from_admin=True)
    messages.success(request, "Good Job, Your work time added.")
    return redirect(reverse('dashboard:admin-dashboard') + '?pages=add_app_day')


@login_first
def schedule_dtime_admin(request):
    email = request.GET.get('email')
    sch_id = request.GET.get('sch_id')

    try:
        doctor = user_info(request)
        admin = Patient.objects.get(email=email)
        wk = AppDay.objects.get(id=sch_id)
        wk.is_booked = True
        wk.save()
        bk = AppAdmin(doctor=doctor, patient=admin, schedule=wk, room_id=random_room_id())
        bk.save()
        EmailThread('email/room_id_email.html', user_info(request).email,
                    {'room_id': bk.room_id, 'name': user_info(request).first_name}).start()
        EmailThread('email/room_id_email.html', bk.patient.email,
                    {'room_id': bk.room_id, 'name': bk.patient.first_name}).start()

        messages.success(request, "Good Job, We have scheduled this specific date for you!")
    except IntegrityError:
        wk = AppDay.objects.get(id=sch_id)
        wk.is_booked = False
        wk.save()

        messages.error(request, "Sorry, We cant schedule specific date for you!")

    return redirect(reverse('dashboard:doctor-dashboard'))


@login_first
def approve_doctor(request, id):
    try:
        doc = Doctor.objects.get(id=id)
        doc.is_verified = True
        doc.save()
        messages.success(request, "Good Job, Doctor Approved!")
    except:
        messages.error(request, "Sorry, Doctor not approved!")
    return redirect(reverse('dashboard:admin-dashboard') + '?pages=doctors_waiting')


def view_cv(request, id):
    doctor = Doctor.objects.get(id=id)

    response = HttpResponse(doctor.document, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="cv.pdf"'
    response['X-Download-Options'] = 'noopen'
    return response


@login_first
def fill_date(request):
    if request.POST.get('fill_date'):
        first_date = request.POST.get('date-first')
        last_date = request.POST.get('date-final')
        list_date = request.POST.get('date-input')

        try:
            rs = date_spliter(list_date)
        except:
            messages.error(request, "Sorry, Please follow free time input format.")
            return redirect(reverse('dashboard:doctor-dashboard') + '?pages=working_day')
        y, m, d = first_date.split('-')

        email = user_info(request).email
        temp_doc = Doctor.objects.get(email=email)

        if last_date == "":
            add_schedule(f"{y}-{m}-{d}", rs, temp_doc)
        else:
            y2, m2, d2 = last_date.split('-')
            print(d, d2)
            for rdt in range(int(d), int(d2) + 1):
                print(rdt, rs)
                add_schedule(f"{y}-{m}-{rdt}", rs, temp_doc)
    messages.success(request, "Good Job, Your work time added.")
    return redirect(reverse('dashboard:doctor-dashboard') + '?pages=working_day')


@login_first
def schedule_dtime(request):
    doctor = request.GET.get('doctor')
    sch_id = request.GET.get('sch_id')

    try:
        pt = user_info(request)
        doctor = Doctor.objects.get(email=doctor)
        wk = WorkingDay.objects.get(id=sch_id)
        wk.is_booked = True
        wk.save()
        bk = Appointment(doctor=doctor, patient=pt, schedule=wk, room_id=random_room_id())
        bk.save()
        EmailThread('email/room_id_email.html', user_info(request).email,
                    {'room_id': bk.room_id, 'name': user_info(request).first_name}).start()
        EmailThread('email/room_id_email.html', bk.doctor.email,
                    {'room_id': bk.room_id, 'name': bk.doctor.first_name}).start()


        messages.success(request, "Good Job, We have scheduled this specific date for you!")
    except IntegrityError:
        wk = WorkingDay.objects.get(id=sch_id)
        wk.is_booked = True
        wk.save()
        messages.error(request, "Sorry, We cant schedule specific date for you!")

    return redirect(reverse('dashboard:patient-dashboard'))
