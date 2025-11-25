from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ProviderProfile, ClientProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = ['business_name', 'ruc', 'address', 'phone', 'bio', 'is_verified', 'rating']

class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['phone', 'address', 'preferences']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Customizes the JWT response to include user details and role.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add extra data to the response
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'role': self.user.role
        }
        return data

# -- Registration Serializers (for Validation) --

class ProviderRegistrationSerializer(serializers.Serializer):
    """
    Validates input for Provider Registration.
    Combines User fields + ProviderProfile fields.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    # Profile fields
    business_name = serializers.CharField(max_length=255)
    ruc = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    bio = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_ruc(self, value):
        if ProviderProfile.objects.filter(ruc=value).exists():
            raise serializers.ValidationError("RUC already registered.")
        return value

class ClientRegistrationSerializer(serializers.Serializer):
    """
    Validates input for Client Registration.
    Combines User fields + ClientProfile fields.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    # Profile fields
    phone = serializers.CharField(max_length=20, required=False)
    address = serializers.CharField(max_length=255, required=False)
    preferences = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
