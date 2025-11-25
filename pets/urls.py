from django.urls import path
from .views import PetListCreateView, PetDetailView

urlpatterns = [
    path('', PetListCreateView.as_view(), name='pet-list-create'), # /api/pets/
    path('<int:pk>/', PetDetailView.as_view(), name='pet-detail'), # /api/pets/1/
]
