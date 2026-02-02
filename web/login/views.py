from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

from .serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
from .models import PasswordResetToken

User = get_user_model()


# 🔐 LOGIN
class LoginView(APIView):

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# 📧 FORGOT PASSWORD (SEND MAIL)
class ForgotPasswordView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.get(email=email)

        # 🔥 Delete old tokens (optional but clean)
        PasswordResetToken.objects.filter(user=user).delete()

        reset_obj = PasswordResetToken.objects.create(user=user)

        reset_link = (
            f"http://localhost:3000/reset-password"
            f"?token={reset_obj.token}"
        )

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password:\n{reset_link}",
            from_email=None,
            recipient_list=[email],
        )

        return Response(
            {"message": "Password reset link sent to email"},
            status=status.HTTP_200_OK
        )


# 🔁 RESET PASSWORD
class ResetPasswordView(APIView):

    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            reset_obj = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"message": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ⏰ Token expiry (15 minutes)
        if reset_obj.created_at < timezone.now() - timedelta(minutes=15):
            reset_obj.delete()
            return Response(
                {"message": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = reset_obj.user
        user.set_password(new_password)
        user.save()

        reset_obj.delete()  # one-time token

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )

