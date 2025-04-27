from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import doctors, bookings, patients_table
from django.urls import reverse
from datetime import datetime
from django.utils.timezone import now, make_aware
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.

def home2(request):
    return render(request,'home2.html')


def validate_user(request):
    if request.method == "POST":
        username = request.POST["user"]
        phone = request.POST["phone"]
        userdata = patients_table.objects.filter(phone=phone)

        # Get the URL to redirect using Django reverse
        redirect_url = reverse('home2')

        if userdata.exists():
            return HttpResponse(f"""
                <script>
                    alert("Phone number already exists: {phone}");
                    window.location.href = "{redirect_url}";
                </script>
            """)
        else:
            da = patients_table(username=username, phone=phone)
            da.save()
            return HttpResponse(f"""
                <script>
                    alert("User created successfully");
                    window.location.href = "{redirect_url}";
                </script>
            """)

    return render(request, 'login2.html')





def book_appointment(request):
    if request.method == 'POST':
        redirect_url = reverse('bookappointment2')
        home_url = reverse('home2')

        try:
            name = request.POST['pname'].strip()
            doctor_id = request.POST['doctor'].strip()
            email = request.POST['email'].strip()
            date = request.POST['date'].strip()
            time = request.POST['time'].strip()
            description = request.POST['desc'].strip()
        except Exception:
            return HttpResponse(f"""
                <script>
                    alert("Please fill all the fields");
                    window.location.href = "{redirect_url}";
                </script>
            """)

        # Check for any empty field
        if not all([name, doctor_id, date, time, description, email]):
            return HttpResponse(f"""
                <script>
                    alert("Please fill all the fields");
                    window.location.href = "{redirect_url}";
                </script>
            """)

        # Convert to datetime and make it timezone-aware
        dt = make_aware(datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M"))
        if dt < now():
            return HttpResponse(f"""
                <script>
                    alert("Please select future time");
                    window.location.href = "{redirect_url}";
                </script>
            """)

        try:
            doctor_obj = doctors.objects.get(id=doctor_id)
        except doctors.DoesNotExist:
            return HttpResponse(f"""
                <script>
                    alert("Doctor not found");
                    window.location.href = "{redirect_url}";
                </script>
            """)

        # Check doctor's working hours
        input_time = datetime.strptime(time, "%H:%M").time()
        if not (doctor_obj.start_time <= input_time <= doctor_obj.end_time):
            return HttpResponse(f"""
                <script>
                    alert("Please book appointment within doctor's working hours");
                    window.location.href = "{redirect_url}";
                </script>
            """)

        if bookings.objects.filter(doctor_name=doctor_obj.name, date=date, time=time).exists():
            return HttpResponse(f"""
                <script>
                    alert("Slot is already booked...choose another time");
                    window.location.href = "{redirect_url}";
                </script>
            """)

        # Check 10-minute gap rule
        if input_time.minute % 10 == 0:
            booking = bookings(
                patient_name=name,
                doctor_name=doctor_obj.name,
                email = email,
                date=date,
                time=time,
                description=description
            )
            booking.save()
            # Send confirmation email to patient
            subject = "Appointment Confirmation - Vcube Hospitals"
            message = f"""
            Dear {name},

            Your appointment has been successfully booked.

            Details:
            Doctor: Dr. {doctor_obj.name}
            Date: {date}
            Time: {time}

            Thank you for choosing Vcube Hospitals.
            We look forward to seeing you!

            Best regards,
            Vcube Hospitals Team
            """

            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )


            return HttpResponse(f"""
                <script>
                    alert("Appointment booked successfully");
                    window.location.href = "{home_url}";
                </script>
            """)
        else:
            return HttpResponse(f"""
                <script>
                    alert("Please book appointments at 10-minute intervals: \\n12:00, 12:10, 12:20, 12:30, etc.");
                    window.location.href = "{redirect_url}";
                </script>
            """)

    dtr = doctors.objects.all()
    return render(request, 'bookappointment2.html', {"dtr": dtr})



def doctors_page(request):
    return render(request,"doctors_page.html")



def appointments(request):
    app = bookings.objects.all()
    return render(request,"appointments.html",{"app":app})


def doctor_appointments(request):
    appints = []  # initialize empty queryset or list
    if request.method == "POST":
        name = request.POST['doctor']
        date = request.POST['date']
        appints = bookings.objects.filter(doctor_name=name, date=date)

    doct = doctors.objects.all()
    return render(request, "doctor_appointments.html", {
        "doctor": doct,
        "appointments": appints
    })

