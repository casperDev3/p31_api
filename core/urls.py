from django.contrib import admin
from django.urls import path, include

PREFIX = 'api/v1'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{PREFIX}/news/', include('news.urls')),
    path(f'{PREFIX}/auth/', include('authentication.urls')),
]
