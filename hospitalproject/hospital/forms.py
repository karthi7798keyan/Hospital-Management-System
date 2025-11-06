from django import forms
from .models import Appointment, Patient, CallbackRequest

class AppointmentForm(forms.ModelForm):
    patient_select = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        required=False,
        empty_label="(New patient)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    patient_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'})
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )
    gender = forms.ChoiceField(
        choices=Patient.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 2})
    )

    class Meta:
        model = Appointment
        fields = ['department', 'doctor', 'date', 'time', 'description']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Reason for Appointment', 'rows': 3}),
        }

    def clean(self):
        cleaned = super().clean()
        patient_selected = cleaned.get('patient_select')
        name = cleaned.get('patient_name')

        if not patient_selected and not name:
            raise forms.ValidationError("Either select an existing patient or provide the new patient's name.")

        if not patient_selected and name:
            if not cleaned.get('age') or not cleaned.get('gender') or not cleaned.get('phone'):
                raise forms.ValidationError("For a new patient please provide age, gender and phone.")

        return cleaned


class CallbackRequestForm(forms.ModelForm):
    class Meta:
        model = CallbackRequest
        fields = ['name', 'phone', 'preferred_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'preferred_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred time to call'}),
        }
