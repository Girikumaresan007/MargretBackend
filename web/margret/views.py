from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Client
from .serializers import ClientSerializers


# 🔹 Base class for Swagger safety
class SwaggerSafeGenericAPIView(GenericAPIView):
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Client.objects.none()
        return Client.objects.all()


class ClientListAPIView(SwaggerSafeGenericAPIView):
    serializer_class = ClientSerializers

    def get(self, request):
        clients = Client.objects.all()
        serializer = self.get_serializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientCreateAPIView(SwaggerSafeGenericAPIView):
    serializer_class = ClientSerializers

    @swagger_auto_schema(request_body=ClientSerializers)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClientRetrieveAPIView(SwaggerSafeGenericAPIView):
    serializer_class = ClientSerializers

    def get(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=404)

        serializer = self.get_serializer(client)
        return Response(serializer.data)


class ClientUpdateAPIView(SwaggerSafeGenericAPIView):
    serializer_class = ClientSerializers

    @swagger_auto_schema(request_body=ClientSerializers)
    def put(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=404)

        serializer = self.get_serializer(client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ClientDeleteAPIView(SwaggerSafeGenericAPIView):

    def delete(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response({"error": "Client not found"}, status=404)

        client.delete()
        return Response({"message": "Client deleted successfully"}, status=204)
