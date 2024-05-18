from django.urls import path
from recommendation.views import *

urlpatterns = [
    path("", re_home, name="re_home"),
    path("predict", re_home, name="predict"),
    path("login", login, name="login"),
]
