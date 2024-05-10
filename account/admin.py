from django.contrib import admin
from account.models import *
from django.contrib.auth.models import Group  # new


admin.site.unregister(Group)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Revoke)

admin.site.site_header = "Tenassist Super Admin"
admin.site.site_title = "Tenassist SuperAdmin Portal"
admin.site.index_title = "Tenassist Super Admin"
