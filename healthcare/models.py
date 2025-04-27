from django.db import models

# Create your models here.




class doctors(models.Model):
    name = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name


class bookings(models.Model):
    patient_name = models.CharField(max_length=20)
    doctor_name = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField()
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.patient_name
    


class patients_table(models.Model):
    username = models.CharField(max_length=20)
    phone = models.BigIntegerField()

    def __str__(self):
        return f"{self.username}  {self.phone}"




    