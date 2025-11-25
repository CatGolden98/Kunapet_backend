from rest_framework import serializers
from .models import Appointment
from services.serializers import ServiceSerializer
from users.serializers import UserSerializer

class AppointmentSerializer(serializers.ModelSerializer):
    # Read-only nested fields for display
    service_details = ServiceSerializer(source='service', read_only=True)
    client_details = UserSerializer(source='client', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'client', 'service', 'date', 'time', 'status', 'notes', 'created_at', 'service_details', 'client_details']
        read_only_fields = ['id', 'client', 'created_at', 'status']

    def create(self, validated_data):
        # Automatically assign the authenticated user as the client
        validated_data['client'] = self.context['request'].user
        return super().create(validated_data)

class AppointmentStatusSerializer(serializers.ModelSerializer):
    """
    Serializer specifically for updating the status of an appointment (for Providers).
    """
    class Meta:
        model = Appointment
        fields = ['status']
