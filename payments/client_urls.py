from django.urls import path
from .views import pay_view, success_view

urlpatterns = [
    path('pay/', pay_view, name='pay'),
    path('success/', success_view, name='payment_result'),
]