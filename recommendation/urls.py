from django.urls import path
from recommendation.views import *

urlpatterns = [
    path("", re_home, name="re_home"),
    path("test", test_page, name="test"),
    path("login", login, name="login"),
    path("interview0", interview0, name="interview0"),
    path("interview1", interview1, name="interview1"),
    path("interview2", interview2, name="interview2"),
    path("interview3", interview3, name="interview3"),
    path("interview4", interview4, name="interview4"),
    path("vom_interview", vom_interview, name="vom_interview"),

    # cough
    path('cough_interview1', cough_interview1, name="cough_interview1"),
    path('cough_interview2', cough_interview2, name="cough_interview2"),
    path('cough_result', cough_result, name='cough_result'),

    # headache
    path("headache_interview1", headache_interview1, name='headache_interview1'),
    path("headache_interview2", headache_interview2, name='headache_interview2'),
    path("headache_interview3", headache_interview3, name='headache_interview3'),
    path("headache_interview4", headache_interview4, name='headache_interview4'),
    path("headache_interview5", headache_interview5, name='headache_interview5'),
    path("headache_result", headache_result, name="headache_result"),
    # fever
    path("fever_interview1", fever_interview1, name='fever_interview1'),
    path("fever_interview2", fever_interview2, name='fever_interview2'),
    path("fever_interview3", fever_interview3, name='fever_interview3'),
    path("fever_interview4", fever_interview4, name='fever_interview4'),
    path("fever_interview5", fever_interview5, name='fever_interview5'),
    path("fever_result", fever_result, name='fever_result'),
    path("recommend", recommend, name='recommend'),
]
