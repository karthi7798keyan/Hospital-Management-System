from rest_framework.permissions import BasePermission

class IsAdminDoctorOrPatient(BasePermission):
    """
    Allows access only to Admin, Doctor, or Patient users
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Admin
        if user.is_staff or user.is_superuser:
            return True

        # Doctor
        if hasattr(user, "doctor"):
            return True

        # Patient
        if hasattr(user, "patient"):
            return True

        return False
