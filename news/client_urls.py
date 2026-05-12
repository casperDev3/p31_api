from django.urls import path
from .views import LandingView, ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='news'),
    path('/<int:pk>/', ArticleDetailView.as_view(), name='news-detail'),
    path('landing/', LandingView.as_view(), name='landing'),
]