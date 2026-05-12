from django.urls import path
from .views import LandingView

urlpatterns = [
    path('landing/', LandingView.as_view(), name='landing'),
]