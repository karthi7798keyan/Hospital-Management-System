from django.urls import path
from .views import AppointmentListAPIView

urlpatterns = [
    path('appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),
]
