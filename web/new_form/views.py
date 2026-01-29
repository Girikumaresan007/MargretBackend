from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Book
from .serializers import BookSerializers


class SwaggerSafeGenericAPIView(GenericAPIView):
    queryset = Book.objects.all()

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Book.objects.none()
        return super().get_queryset()


class BookListAPIView(SwaggerSafeGenericAPIView):
    serializer_class = BookSerializers

    def get(self, request):
        books = Book.objects.all()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCreateAPIView(GenericAPIView):
    serializer_class = BookSerializers

    @swagger_auto_schema(request_body=BookSerializers)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


class BookRetrieveAPIView(SwaggerSafeGenericAPIView):
    serializer_class = BookSerializers

    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookUpdateAPIView(SwaggerSafeGenericAPIView):
    serializer_class = BookSerializers

    @swagger_auto_schema(request_body=BookSerializers)
    def put(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        serializer = self.get_serializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDeleteAPIView(SwaggerSafeGenericAPIView):
    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=404)

        book.delete()
        return Response(
            {"message": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
