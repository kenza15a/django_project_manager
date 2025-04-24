from django.contrib import admin
from django.urls import path, include
from project_manager.views import login_view, me_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Project Manager API",
        default_version='v1',
        description="API de gestion des utilisateurs et projets",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("api/login/", login_view),
    path("api/me/", me_view),
    path('admin/', admin.site.urls),
    path('api/', include('project_manager.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
