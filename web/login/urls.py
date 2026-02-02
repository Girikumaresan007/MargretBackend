from django.urls import path
from .views import LoginView, ForgotPasswordView, ResetPasswordView

app_name = "web"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
]
