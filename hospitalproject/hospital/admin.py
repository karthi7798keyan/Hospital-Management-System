from django.contrib import admin
from django import forms
from .models import Department, Doctor, Appointment, Invoice, Prescription, CallbackRequest


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialization', 'department', 'experience')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'date', 'time', 'status', 'token_number')
    list_filter = ('status', 'department', 'doctor')
    search_fields = ('patient__name', 'doctor__name')


class InvoiceAdminForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'consultation_fee': forms.NumberInput(attrs={'step': 50, 'min': 0}),
            'medicine_cost': forms.NumberInput(attrs={'step': 50, 'min': 0}),
            'other_charges': forms.NumberInput(attrs={'step': 50, 'min': 0}),
        }


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceAdminForm
    list_display = (
        'appointment',
        'consultation_fee',
        'medicine_cost',
        'other_charges',
        'total_amount',
        'date_issued'
    )
    search_fields = ('appointment__patient__name',)
    list_filter = ('date_issued',)
    readonly_fields = ('total_amount',)


    def save_model(self, request, obj, form, change):
        obj.total_amount = (
            (obj.consultation_fee or 0)
            + (obj.medicine_cost or 0)
            + (obj.other_charges or 0)
        )
        super().save_model(request, obj, form, change)

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'diagnosis', 'date_issued')
    search_fields = ('appointment__patient__name', 'diagnosis')

@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'preferred_time')
    search_fields = ('name', 'phone')
