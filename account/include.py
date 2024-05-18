from threading import Thread

from .models import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from appointment.models import Appointment


def user_role(request):
    status = request.session.get('user-role', None)
    return status


def user_info(request):
    email = request.session.get("email", None)
    us = None
    if email is not None:
        try:
            ls_us = Patient.objects.filter(email=email)
            ls_dr = Doctor.objects.filter(email=email)
            if len(ls_us) > 0:
                us = ls_us[0]
            elif len(ls_dr) > 0:
                us = ls_dr[0]
        except:
            pass
    return us


class EmailThread(Thread):
    def __init__(self, link, email_to, context):
        self.email_to = email_to
        self.link = link
        self.context = context
        Thread.__init__(self)

    def run(self):
        html_content = render_to_string(self.link, self.context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Tenalink System',
            text_content,
            'ayalkbettesfahun@gmail.com',
            [self.email_to],
        )
        email.attach_alternative(html_content, "text/html")
        if email.send() > 0:
            return True
        else:
            return False


def send_email(link, to, content):
    try:
        html_content = render_to_string(link, content)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            'Tenalink System',
            text_content,
            'ayalkbettesfahun@gmail.com',
            to,
        )
        email.attach_alternative(html_content, "text/html")
        return email.send() > 0
    except:
        return False


def automate_email(request):
    app = Appointment.objects.filter()
    for ap in app:
        if not ap.is_notified:
            if (ap.left_time.total_seconds() > 0) and (ap.left_time.total_seconds() < 1800):

                EmailThread('email/appointment_reminder.html', ap.patient.email, {'name': ap.patient.first_name}).start()
                EmailThread('email/appointment_reminder.html', ap.doctor.email, {'name': ap.doctor.first_name}).start()

                ap.is_notified = True
                ap.save()
