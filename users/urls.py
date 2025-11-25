from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, 
    ProviderRegisterView, 
    ClientRegisterView,
    MeView
)

urlpatterns = [
    # Auth
    path('auth/register/provider/', ProviderRegisterView.as_view(), name='register_provider'),
    path('auth/register/client/', ClientRegisterView.as_view(), name='register_client'),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User info
    path('auth/me/', MeView.as_view(), name='user_me'),
]
