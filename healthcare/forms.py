from . models import patients_table,doctors, bookings
from django import forms


class patients_table_form(forms.Form):
    class Meta:
        model = patients_table
        fields = '__all__'