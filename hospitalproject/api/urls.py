from django.urls import path
from .views import AppointmentListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Get access & refresh tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh access token
]
