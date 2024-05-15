from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


app_name = 'tenassist'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls')),
    path('chat/', include('webrtc.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('recommend/', include('recommendation.urls'), name="recommend"),
    path('appointment/', include('appointment.urls')),
    path('', include('account.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)