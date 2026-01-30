from django.urls import path
from .views import (
    BookListAPIView,
    BookCreateAPIView,
    BookRetrieveAPIView,
    BookUpdateAPIView,
    BookDeleteAPIView,
    BookConfirmAPIView,
    DashboardSummaryAPIView,
    BookingsOverTimeAPIView,
    PackagePopularityAPIView,
    EventTypeDistributionAPIView,
    AttendeeInsightsAPIView,
)

urlpatterns = [
    # 📘 BOOKS (CRUD)
    path("books/", BookListAPIView.as_view()),
    path("books/create/", BookCreateAPIView.as_view()),
    path("books/<int:pk>/", BookRetrieveAPIView.as_view()),
    path("books/<int:pk>/update/", BookUpdateAPIView.as_view()),
    path("books/<int:pk>/delete/", BookDeleteAPIView.as_view()),
    path("books/<int:pk>/confirm/", BookConfirmAPIView.as_view()),

    # 📊 DASHBOARD
    path("dashboard/summary/", DashboardSummaryAPIView.as_view()),
    path("dashboard/bookings-over-time/", BookingsOverTimeAPIView.as_view()),
    path("dashboard/package-popularity/", PackagePopularityAPIView.as_view()),
    path("dashboard/event-type-distribution/", EventTypeDistributionAPIView.as_view()),
    path("dashboard/attendee-insights/", AttendeeInsightsAPIView.as_view()),
]
