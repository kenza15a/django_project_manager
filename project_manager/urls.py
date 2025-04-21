from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ProjectViewSet,
    RegisterUserView, UserDetailView, ProjectDetailView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)

urlpatterns = [

    path('users/register/', RegisterUserView.as_view(), name='user-register'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('projects/<int:id>/<str:username>/',
         ProjectDetailView.as_view(), name='project-detail'),
    # Router must come LAST sinon django va le prioriser
    path('', include(router.urls)),
]
