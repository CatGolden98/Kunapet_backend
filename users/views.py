from django.db import transaction
from rest_framework import status, views, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .models import ProviderProfile, ClientProfile
from .serializers import (
    CustomTokenObtainPairSerializer,
    ProviderRegistrationSerializer,
    ClientRegistrationSerializer,
    UserSerializer,
    ProviderProfileSerializer,
    ClientProfileSerializer
)

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Login endpoint that returns Token + User Info + Role.
    """
    serializer_class = CustomTokenObtainPairSerializer


class ProviderRegisterView(views.APIView):
    """
    POST /api/auth/register/provider/
    Atomic transaction: Create User (Provider) + ProviderProfile.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ProviderRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                with transaction.atomic():
                    # 1. Create User
                    user = User.objects.create_user(
                        email=data['email'],
                        password=data['password'],
                        username=data['email'], # utilizing email as username
                        role=User.Role.PROVIDER
                    )

                    # 2. Create ProviderProfile
                    ProviderProfile.objects.create(
                        user=user,
                        business_name=data['business_name'],
                        ruc=data['ruc'],
                        address=data['address'],
                        phone=data['phone'],
                        bio=data.get('bio', '')
                    )
                    
                    # Generate Tokens
                    tokens = get_tokens_for_user(user)
                    
                    response_data = {
                        'user': UserSerializer(user).data,
                        'tokens': tokens,
                        'message': 'Provider registered successfully.'
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Transaction rolls back automatically on exception
                return Response(
                    {'error': f'Registration failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientRegisterView(views.APIView):
    """
    POST /api/auth/register/client/
    Atomic transaction: Create User (Client) + ClientProfile.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ClientRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                with transaction.atomic():
                    # 1. Create User
                    user = User.objects.create_user(
                        email=data['email'],
                        password=data['password'],
                        username=data['email'],
                        role=User.Role.CLIENT
                    )

                    # 2. Create ClientProfile
                    ClientProfile.objects.create(
                        user=user,
                        phone=data.get('phone', ''),
                        address=data.get('address', ''),
                        preferences=data.get('preferences', '')
                    )
                    
                    # Generate Tokens
                    tokens = get_tokens_for_user(user)
                    
                    response_data = {
                        'user': UserSerializer(user).data,
                        'tokens': tokens,
                        'message': 'Client registered successfully.'
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    {'error': f'Registration failed: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(views.APIView):
    """
    GET /api/auth/me/
    Returns current user info and their specific profile data.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'user': UserSerializer(user).data
        }

        # Attach profile data based on role
        if user.role == User.Role.PROVIDER:
            try:
                profile = user.provider_profile
                data['profile'] = ProviderProfileSerializer(profile).data
            except ProviderProfile.DoesNotExist:
                data['profile'] = None
                
        elif user.role == User.Role.CLIENT:
            try:
                profile = user.client_profile
                data['profile'] = ClientProfileSerializer(profile).data
            except ClientProfile.DoesNotExist:
                data['profile'] = None

        return Response(data, status=status.HTTP_200_OK)
