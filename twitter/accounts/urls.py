from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import register_phase_one, VerifyEmail, register_phase_two
from django.urls import path

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("registerE/", register_phase_one),
    path('email-verify', VerifyEmail.as_view(), name='verify_email'),
    path('register/', register_phase_two),
]
