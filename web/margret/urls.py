from django.urls import path
from .views import (
    ClientListAPIView,
    ClientCreateAPIView,
    ClientRetrieveAPIView,
    ClientUpdateAPIView,
    ClientDeleteAPIView,
)

urlpatterns = [
    path('', ClientListAPIView.as_view()),
    path('create/', ClientCreateAPIView.as_view()),
    path('<int:pk>/', ClientRetrieveAPIView.as_view()),
    path('<int:pk>/update/', ClientUpdateAPIView.as_view()),
    path('<int:pk>/delete/', ClientDeleteAPIView.as_view()),
]
