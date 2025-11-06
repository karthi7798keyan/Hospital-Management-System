from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    head_of_department = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    experience = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='doctors', blank=True, null=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    date_registered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    description = models.TextField(blank=True, null=True)
    token_number = models.IntegerField(default=1000)

    def save(self, *args, **kwargs):
        if not self.token_number:
            last_token = Appointment.objects.aggregate(models.Max('token_number'))['token_number__max']
            self.token_number = int(last_token) + 1 if last_token else 1000
        super().save(*args, **kwargs)

    def __str__(self):
        patient_name = self.patient.name if self.patient else "Unknown Patient"
        return f"Appointment - {patient_name} ({self.date})"

class Invoice(models.Model):
    appointment = models.OneToOneField('Appointment', on_delete=models.CASCADE)
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    medicine_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    other_charges = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_issued = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total_amount = (
            (self.consultation_fee or 0)
            + (self.medicine_cost or 0)
            + (self.other_charges or 0)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice for {self.appointment.patient.name} (Token {self.appointment.token_number})"

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True, null=True)
    medicines = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)
    date_issued = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.name} (Token {self.appointment.token_number})"

class CallbackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    preferred_time = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"Callback from {self.name} ({self.phone})"


