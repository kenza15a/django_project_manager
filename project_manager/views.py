from rest_framework import viewsets, filters
from .models import User, Project
from .serializers import UserSerializer, ProjectSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class StandardPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

# viewsets pour les operations crud


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['username', 'email']
    ordering_fields = ['username', 'email']


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = StandardPagination
    filter_backends = [filters.OrderingFilter,
                       filters.SearchFilter, DjangoFilterBackend]
    
    search_fields = ['title']
    ordering_fields = ['title', 'created_at']
    filterset_fields = ['owner','title']

    def perform_create(self, serializer):
        user = self.request.user

        # S'assurer que l'utilisateur est connecté
        if not user or not user.is_authenticated:
            raise PermissionDenied("Authentication required to create a project.")

        # Si c'est un SimpleLazyObject, le convertir
        if not isinstance(user, User):
            user = User.objects.get(pk=user.pk)

        # Créer le projet
        serializer.save(owner=user)


# vues personnalisées
# Vue pour /api/users/register/


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vue pour /api/users/<username>/


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'
# gestion des projets
# Permission personnalisée : seul le propriétaire peut modifier/supprimer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Lecture : autorisée pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        # Modification : autorisée uniquement pour le propriétaire
        return obj.owner.username == view.kwargs.get("username")

# Vue personnalisée pour un projet donné


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'id'

    def get_object(self):
        obj = get_object_or_404(
            Project,
            id=self.kwargs['id'], 
            owner__username=self.kwargs['username']
        )
        self.check_object_permissions(self.request, obj)
        return obj
