from rest_framework import serializers
from .models import Service
from users.models import ProviderProfile

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Get the provider profile associated with the current user
        user = self.context['request'].user
        try:
            provider_profile = user.provider_profile
        except ProviderProfile.DoesNotExist:
            raise serializers.ValidationError("Only registered providers can create services.")
        
        validated_data['provider'] = provider_profile
        return super().create(validated_data)
