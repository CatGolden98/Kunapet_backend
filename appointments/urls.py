from django.urls import path
from .views import AppointmentListCreateView, AppointmentDetailView

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'), # /api/appointments/
    path('<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'), # /api/appointments/1/
]
