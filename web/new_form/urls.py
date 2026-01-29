from django.urls import path
from .views import (
    BookListAPIView,
    BookCreateAPIView,
    BookRetrieveAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView,
)

urlpatterns = [
    path('', BookListAPIView.as_view()),
    path('create/', BookCreateAPIView.as_view()),
    path('<int:pk>/', BookRetrieveAPIView.as_view()),
    path('<int:pk>/update/', BookUpdateAPIView.as_view()),
    path('<int:pk>/delete/', BookDeleteAPIView.as_view()),
]
