"""
URL configuration for hospitalproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('appointment',views.appointment,name='appointment'),
    path('department',views.department,name='department'),
    path('doctor',views.doctor,name='doctor'),
    path('invoices', views.invoice_list, name='invoice_list'),
    path('patient',views.patient,name='patient'),
    path('prescription',views.prescription,name='prescription'),

    path('blog', views.future_page, name='future_page'),
    path('careers', views.future_page, name='future_page'),
    path('faqs', views.future_page, name='future_page'),
    path('privacy policy', views.future_page, name='future_page'),
    path('about', views.future_page, name='future_page'),

    path('cancel/<int:pk>', views.cancel_appointment, name='cancel_appointment'),

    path('request-callback', views.request_callback, name='request_callback'),

    path('appointment/<int:appointment_id>/pdf/', views.download_pdf, name='download_pdf'),
]

