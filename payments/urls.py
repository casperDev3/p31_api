from django.urls import path
from .views import pay_view, liqpay_callback, success_view

urlpatterns = [
    path('pay/', pay_view, name='pay'),
    path('callback/', liqpay_callback, name='liqpay_callback'),
    path('success/', success_view, name='payment_result'),
]