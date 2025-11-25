from rest_framework import generics, permissions
from .models import Pet
from .serializers import PetSerializer

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access/edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class PetListCreateView(generics.ListCreateAPIView):
    """
    GET: List all pets belonging to the authenticated user.
    POST: Create a new pet for the authenticated user.
    """
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the pets owned by the current user
        return Pet.objects.filter(owner=self.request.user)

class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, PATCH, DELETE a specific pet.
    Only the owner can perform these actions.
    """
    serializer_class = PetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Pet.objects.all()
