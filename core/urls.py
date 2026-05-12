from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

PREFIX_API = 'api/v1'

urlpatterns = [
    path('', include('static.client_urls')),
    path('admin/', admin.site.urls),
    path('news/', include('news.client_urls')),
    path(f'{PREFIX_API}/graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path(f'{PREFIX_API}/news/', include('news.urls')),
    path(f'{PREFIX_API}/auth/', include('authentication.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)