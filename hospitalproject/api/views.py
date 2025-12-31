from rest_framework.generics import ListAPIView
from hospital.models import Appointment
from .serializers import AppointmentSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdminDoctorOrPatient


class AppointmentListAPIView(ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsAdminDoctorOrPatient]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Appointment.objects.all()

        if hasattr(user, "doctor"):
            return Appointment.objects.filter(doctor=user.doctor)

        if hasattr(user, "patient"):
            return Appointment.objects.filter(patient=user.patient)

        return Appointment.objects.none()


