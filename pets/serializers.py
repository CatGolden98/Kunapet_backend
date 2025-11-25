from rest_framework import serializers
from .models import Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'species', 'breed', 'birth_date', 'gender', 'weight', 'photo', 'medical_history', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Automatically assign the owner from the context (request user)
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)
