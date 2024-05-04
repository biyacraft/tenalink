from django.shortcuts import render, redirect, reverse
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import roomMember
from account.include import user_info, user_role
import random
import time
import json


# Create your views here.

def getToken(request):
    APP_ID = "484e7765377f417fa9f98b2a096f2494"
    APP_CERTIFICATE = "976c6eb6a7d4482fb5a57bacc2cf47c5"
    CHANNEL_NAME = request.GET.get('channel')
    uid = random.randint(1, 230)

    expiration_time_in_seconds = 3600 * 24
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(APP_ID, APP_CERTIFICATE, CHANNEL_NAME, uid, role, privilege_expired_ts)
    return JsonResponse({'token': token, 'uid': uid}, safe=False)


def index(request):

    return redirect(reverse(f"dashboard:{user_role(request) if user_role(request) else 'patient'}-dashboard") + "?pages=chat")


@csrf_exempt
def createUser(request):
    data = json.loads(request.body)
    member, created = roomMember.objects.get_or_create(name=data['name'], room_name=data['room_name'], uid=data['uid'])
    return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('uid')
    room_name = request.GET.get('room_name')

    member = roomMember.objects.get(room_name=room_name, uid=uid)
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    try:
        member = roomMember.objects.get(name=data['name'], room_name=data['room_name'], uid=data['uid'])
        member.delete()
    except:
        pass
    return JsonResponse({'name': "member deleted!"}, safe=False)
