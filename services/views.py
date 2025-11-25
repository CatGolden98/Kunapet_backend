from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Service
from .serializers import ServiceSerializer
from users.models import ProviderProfile

class IsProvider(permissions.BasePermission):
    """
    Permission check for Providers.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'provider'

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.provider.user == request.user

class ServiceListCreateView(generics.ListCreateAPIView):
    """
    GET: List all services (Publicly accessible or filtered).
    POST: Create a new service (Only Providers).
    """
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProvider]

    def get_queryset(self):
        # Optional: Filter by provider_id if passed in URL params
        queryset = Service.objects.filter(is_active=True)
        provider_id = self.request.query_params.get('provider_id')
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        return queryset

class ServiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve service details.
    PUT/PATCH/DELETE: Only the owner (Provider) can modify.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
