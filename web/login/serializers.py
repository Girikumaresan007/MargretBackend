from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


# 🔐 LOGIN
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")

        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "is_admin": user.is_staff,
            },
        }


# 📧 FORGOT PASSWORD
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return email


# 🔁 RESET PASSWORD
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(
        min_length=8,
        write_only=True
    )

    def validate_new_password(self, value):
        if not any(c.isupper() for c in value):
            raise serializers.ValidationError("Password must contain an uppercase letter")
        if not any(c.islower() for c in value):
            raise serializers.ValidationError("Password must contain a lowercase letter")
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError("Password must contain a number")
        if not any(c in "@$!%*?&" for c in value):
            raise serializers.ValidationError("Password must contain a special character")
        return value
