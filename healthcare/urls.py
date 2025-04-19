from django.urls import path
from . import views

urlpatterns = [
    path("home2/",views.home2,name='home2'),
    path("login/",views.validate_user,name="validate"),
    path("bookapp/",views.book_appointment,name = "bookappointment2"),
    path("doctors/",views.doctors_page, name="doctorspage"),
    path("appointments/",views.appointments,name="appointments"),
    path("doctorapp/",views.doctor_appointments,name="doctorappointments")
]