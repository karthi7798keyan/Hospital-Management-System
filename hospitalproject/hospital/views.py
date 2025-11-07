from django.shortcuts import render, redirect, get_object_or_404

from django.core.paginator import Paginator
from .models import Department, Doctor, Appointment, Patient, Invoice, Prescription
from .forms import AppointmentForm
from django.http import HttpResponse
from fpdf import FPDF
from io import BytesIO

from django.contrib import messages
from .models import CallbackRequest


def index(request):
    return render(request, 'index.html')


def department(request):
    departments = Department.objects.all()
    return render(request, 'department.html', {'departments': departments})


def doctor(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor.html', {'doctors': doctors})


def patient(request):
    appointment = None
    token = None
    error = None

    if request.method == 'POST':
        token = request.POST.get('token')
        try:
            token_number = int(token)
            appointment = Appointment.objects.get(token_number=token_number)
        except ValueError:
            error = "Token must be a valid number."
        except Appointment.DoesNotExist:
            error = f"No appointment found for Token {token}"

    return render(request, 'patient.html', {
        'appointment': appointment,
        'token': token,
        'error': error
    })


def appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            patient_obj = form.cleaned_data.get('patient_select')
            if not patient_obj:
                patient_obj = Patient.objects.create(
                    name=form.cleaned_data['patient_name'],
                    age=form.cleaned_data['age'],
                    gender=form.cleaned_data['gender'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'] or ''
                )

            appointment = form.save(commit=False)
            appointment.patient = patient_obj

            latest = Appointment.objects.order_by('-token_number').first()
            appointment.token_number = 1000 if not latest else int(latest.token_number) + 1
            appointment.status = 'Pending'
            appointment.save()

            messages.success(
                request,
                f"Appointment booked successfully! Your Token Number is {appointment.token_number}"
            )
            return redirect('appointment')
    else:
        form = AppointmentForm()

    return render(request, 'appointment.html', {'form': form})


def prescription(request):
    appointment = None
    invoice = None
    prescription = None
    error = None

    if request.method == "POST":
        token = request.POST.get("token")
        if not token.isdigit():
            error = "Invalid token number. Please enter numeric values only."
        else:
            try:
                appointment = Appointment.objects.get(token_number=token)
                invoice = Invoice.objects.filter(appointment=appointment).first()
                prescription = Prescription.objects.filter(appointment=appointment).first()
            except Appointment.DoesNotExist:
                error = f"No appointment found for Token {token}"

    context = {
        'appointment': appointment,
        'invoice': invoice,
        'prescription': prescription,
        'error': error
    }
    return render(request, 'prescription.html', context)


def invoice_list(request):
    invoices = Invoice.objects.all().select_related(
        'appointment__patient', 'appointment__doctor'
    ).order_by('-date_issued')

    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'invoice.html', {'page_obj': page_obj})


def future_page(request):
    return render(request, 'future_page.html')


def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if appointment.status != 'Cancelled':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(
            request,
            f"Appointment for {appointment.patient.name} has been cancelled successfully."
        )
    else:
        messages.info(request, "This appointment is already cancelled.")
    return redirect('patient')


def request_callback(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        preferred_time = request.POST.get('preferred_time', '').strip()

        if not name or not phone or not preferred_time:
            messages.error(request, "Please fill all required fields for callback.")
            return redirect('index')

        CallbackRequest.objects.create(
            name=name,
            phone=phone,
            preferred_time=preferred_time
        )

        messages.success(request, "Your callback request has been submitted successfully!")
        return redirect('index')

    return redirect('index')


def download_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    invoice = getattr(appointment, 'invoice', None)
    prescription = getattr(appointment, 'prescription', None)

    pdf = FPDF()
    pdf.add_page()


    pdf.image('static/images/logo.png', x=80, y=10, w=50)


    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Hospital Management System", ln=True, align='C')
    pdf.ln(5)


    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Token Number: {appointment.token_number}", ln=True)
    pdf.cell(0, 10, f"Appointment Date: {appointment.date}", ln=True)
    pdf.ln(5)


    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Patient Details:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, f"""
                    Name: {appointment.patient.name if appointment.patient else "N/A"}
                    Age: {appointment.patient.age if appointment.patient else "N/A"}
                    Gender: {appointment.patient.gender if appointment.patient else "N/A"}
                    Phone: {appointment.patient.phone if appointment.patient else "N/A"}
                    Address: {appointment.patient.address if appointment.patient else "N/A"}
            """)
    pdf.ln(3)


    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Appointment Details:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 8, f"""
Doctor: {appointment.doctor.name}
Department: {appointment.department.name}
Time: {appointment.time}
Status: {appointment.status}
Description: {appointment.description or "N/A"}
""")
    pdf.ln(3)

    if invoice:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Invoice Details:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"""
Consultation Fee: {invoice.consultation_fee}
Medicine Cost: {invoice.medicine_cost}
Other Charges: {invoice.other_charges}
Total Amount: {invoice.total_amount}
Date Issued: {invoice.date_issued}
                                            """)
        pdf.ln(3)

    if prescription:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Prescription Details:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 8, f"""
Diagnosis: {prescription.diagnosis or "N/A"}
Medicines: {prescription.medicines or "N/A"}
Advice: {prescription.advice or "N/A"}
Date Issued: {prescription.date_issued}
                                                """)
        pdf.ln(3)


    pdf.set_font("Arial", 'I', 14)
    pdf.multi_cell(0, 8, "We wish you a speedy recovery! Get well soon and take care of your health.")
    pdf.ln(5)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="appointment_{appointment.id}.pdf"'
    return response
