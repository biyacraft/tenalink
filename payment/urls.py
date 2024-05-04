from django.urls import path
from .views import home, payment_with_cart, payment_with_express, success, cancel, ipn

app_name = 'payment'
urlpatterns = [
    path('', home, name='home'),
    path('with-express/', payment_with_express, name='express-payment'),
    path('with-cart/', payment_with_cart, name='cart-payment'),
    path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('ipn/', ipn, name='ipn')
]