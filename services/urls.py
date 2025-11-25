from django.urls import path
from .views import ServiceListCreateView, ServiceDetailView

urlpatterns = [
    path('', ServiceListCreateView.as_view(), name='service-list-create'), # /api/services/
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'), # /api/services/1/
]
