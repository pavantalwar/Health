from django.contrib import admin
from . models import patients_table,bookings,doctors
# Register your models here.




@admin.register(bookings)
class bookingAdmin(admin.ModelAdmin):
    list_display = ("id","patient_name","doctor_name","date","time","email")

@admin.register(patients_table)
class PatientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone')

@admin.register(doctors)
class doctorAdmin(admin.ModelAdmin):
    list_display = ("id","name","start_time","end_time")