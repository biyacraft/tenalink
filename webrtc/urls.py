from django.urls import path
from webrtc.views import *

app_name = 'chat'
urlpatterns = [
    path('', index, name='index'),
    path('get_token/', getToken, name='get_token'),
    path('create_member/', createUser, name='create_member'),
    path('get_member/', getMember, name='get_member'),
    path('delete_member/', deleteMember, name='delete_member'),
]