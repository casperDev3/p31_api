from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet, TagViewSet, CommentViewSet, LandingView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'comments', CommentViewSet)
router.register('', ArticleViewSet)


urlpatterns = [
    path('landing/', LandingView.as_view()),
    path('', include(router.urls))
]