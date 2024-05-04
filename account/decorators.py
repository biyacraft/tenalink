from django.shortcuts import redirect
from account.include import user_info, user_role
from django.contrib import messages


def login_first(view_func):
    def wrapper(request, *args, **kwargs):
        if user_info(request) is None:
            messages.error(request, "You are not logged in!, Please login first to access the page!")
            return redirect('account:login')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper


def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_role(request) == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Admins' only allowed to access this page!")
            return redirect('account:login')

    return wrapper


def patient_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_role(request) == 'patient':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Patients' only allowed to access this page!")
            return redirect('account:login')

    return wrapper


def doctor_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_role(request) == 'doctor':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Doctors' only allowed to access this page!")
            return redirect('account:login')

    return wrapper

def your_view_only(view_func):
    def wrapper(request, *args, **kwargs):
        if user_role(request) is None:
            messages.error(request, "Sorry, Please login to access pages.")
            return redirect('account:login')
        else:
            flag = user_role(request)
            if flag == 'costumer':
                flag = 'user'
            return redirect(f"post:{flag}-dashboard")
            # return view_func(request, *args, **kwargs)

    return wrapper
