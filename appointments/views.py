from rest_framework import generics, permissions, filters
from django.db.models import Q
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentStatusSerializer

class IsOwnerOrProvider(permissions.BasePermission):
    """
    Clients see their own appointments.
    Providers see appointments for their services.
    """
    def has_object_permission(self, request, view, obj):
        # Check if user is the client who booked
        if obj.client == request.user:
            return True
        # Check if user is the provider of the service
        if obj.service.provider.user == request.user:
            return True
        return False

class AppointmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List appointments.
         - Clients see only their bookings.
         - Providers see bookings for ALL their services.
    POST: Book a new appointment (Client only).
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'client':
            return Appointment.objects.filter(client=user)
        elif user.role == 'provider':
            # Filter appointments where the service belongs to this provider
            return Appointment.objects.filter(service__provider__user=user)
        return Appointment.objects.none()

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: View details.
    PUT/PATCH: 
        - Clients can edit details (notes, time) if pending.
        - Providers can change STATUS (confirm/cancel).
    DELETE: Cancel appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrProvider]

    def get_serializer_class(self):
        # If PATCH request and user is provider, use Status Serializer
        if self.request.method == 'PATCH' and self.request.user.role == 'provider':
            return AppointmentStatusSerializer
        return AppointmentSerializer
