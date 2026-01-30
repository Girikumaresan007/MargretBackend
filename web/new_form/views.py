from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from .models import Book
from .serializers import BookSerializers
@method_decorator(csrf_exempt, name="dispatch")
class BookConfirmAPIView(APIView):

    def patch(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        if book.confirmed:
            return Response(
                {"message": "Booking already confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.confirmed = True
        book.confirmed_at = now()
        book.save()

        return Response(
            {"message": "Booking confirmed successfully"},
            status=status.HTTP_200_OK
        )
class DashboardSummaryAPIView(APIView):

    def get(self, request):
        total_bookings = Book.objects.count()
        confirmed_bookings = Book.objects.filter(confirmed=True).count()

        avg_attendance = (
            Book.objects.aggregate(avg=Avg("attendees"))["avg"] or 0
        )

        popular_package = (
            Book.objects
            .values("package_name")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )

        return Response({
            "total_bookings": total_bookings,
            "contact_requests": total_bookings,  # placeholder
            "confirm_booking": confirmed_bookings,
            "avg_attendance": round(avg_attendance),
            "popular_package": popular_package["package_name"] if popular_package else "-"
        })
class BookingsOverTimeAPIView(APIView):

    def get(self, request):
        data = (
            Book.objects
            .annotate(month=TruncMonth("event_date"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        return Response([
            {
                "month": item["month"].strftime("%b %Y"),
                "bookings": item["total"]
            }
            for item in data
        ])
class PackagePopularityAPIView(APIView):

    def get(self, request):
        return Response(
            Book.objects
            .values("package_name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
class EventTypeDistributionAPIView(APIView):

    def get(self, request):
        return Response(
            Book.objects
            .values("event_type")
            .annotate(total=Count("id"))
        )
class AttendeeInsightsAPIView(APIView):

    def get(self, request):
        return Response({
            "0–50": Book.objects.filter(attendees__lte=50).count(),
            "51–100": Book.objects.filter(attendees__range=(51, 100)).count(),
            "101–150": Book.objects.filter(attendees__range=(101, 150)).count(),
            "151–200": Book.objects.filter(attendees__range=(151, 200)).count(),
            "201–250": Book.objects.filter(attendees__range=(201, 250)).count(),
            "250+": Book.objects.filter(attendees__gt=250).count(),
        })
class SwaggerSafeGenericAPIView(GenericAPIView):
    queryset = Book.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Book.objects.none()
        return super().get_queryset()
class BookListAPIView(SwaggerSafeGenericAPIView):
    serializer_class = BookSerializers

    def get(self, request):
        books = Book.objects.all().order_by("-id")
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
@method_decorator(csrf_exempt, name="dispatch")
class BookCreateAPIView(GenericAPIView):
    serializer_class = BookSerializers

    @swagger_auto_schema(request_body=BookSerializers)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class BookRetrieveAPIView(SwaggerSafeGenericAPIView):
    serializer_class = BookSerializers

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        serializer = self.get_serializer(book)
        return Response(serializer.data)
@method_decorator(csrf_exempt, name="dispatch")
class BookUpdateAPIView(SwaggerSafeGenericAPIView):
    serializer_class = BookSerializers

    @swagger_auto_schema(request_body=BookSerializers)
    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        serializer = self.get_serializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
@method_decorator(csrf_exempt, name="dispatch")
class BookDeleteAPIView(SwaggerSafeGenericAPIView):

    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Booking not found"}, status=404)

        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
