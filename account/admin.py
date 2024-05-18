from django.contrib import admin
from account.models import *
from django.contrib.auth.models import Group  # new


admin.site.unregister(Group)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Revoke)

admin.site.site_header = "Tenalink Super Admin"
admin.site.site_title = "Tenalink SuperAdmin Portal"
admin.site.index_title = "Tenalink Super Admin"
