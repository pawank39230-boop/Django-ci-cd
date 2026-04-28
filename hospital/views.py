from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from.models import *


def About(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    return render(request, 'index.html')


def Login(request):
    error = ''

    if request.method == 'POST':
        u = request.POST.get('uname')
        p = request.POST.get('pwd')

        user = authenticate(username=u, password=p)

        if user is not None and user.is_staff:
            login(request, user)
            error = 'no'
        else:
            error = 'yes'
    d = {'error': error }
    return render(request, 'login.html', d)


def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')


def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')

    doc = Doctor.objects.all()
    d = {'doc': doc}

    return render(request, 'view_doctor.html', d)


from django.shortcuts import render, redirect
from .models import Doctor


def Add_Doctor(request):
    error = ""

    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        n = request.POST.get('name')
        c = request.POST.get('contact')
        sp = request.POST.get('special')

        try:
            Doctor.objects.create(name=n, mobile=c, special=sp)
            error = 'no'
        except:
            error = 'yes'

    d = {'error': error}
    return render(request, 'add_doctor.html', d)



def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')


def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')

    pat = Patient.objects.all()
    d = {'pat': pat}

    return render(request, 'view_patient.html', d)




def Add_Patient(request):
    error = ""

    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        n = request.POST.get('name')
        g = request.POST.get('gender')
        m = request.POST.get('mobile')
        a = request.POST.get('address')


        try:
            Patient.objects.create(name=n, gender=g, mobile=m, address=a)
            error = 'no'
        except:
            error = 'yes'

    d = {'error': error}
    return render(request, 'add_patient.html', d)



def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')



def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')

    appoint = Appointment.objects.all()
    d = {'appoint':appoint}

    return render(request, 'view_appointment.html', d)




def Add_Appointment(request):
    error = ""

    if not request.user.is_staff:
        return redirect('login')

    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()

    if request.method == 'POST':
        print("POST METHOD CALLED")
        print(request.POST)

        try:
            d = request.POST.get('doctor')
            p = request.POST.get('patient')
            d1 = request.POST.get('date')
            t1 = request.POST.get('time')

            doctor = Doctor.objects.get(id=d)
            patient = Patient.objects.get(id=p)

            Appointment.objects.create(
                doctor=doctor,
                patient=patient,
                date1=d1,
                time1=t1
            )

            print("SAVED SUCCESSFULLY")
            error = 'no'

        except Exception as e:
            print("ERROR:", e)
            error = 'yes'

    return render(request, 'add_appointment.html', {
        'doctor': doctor1,
        'patient': patient1,
        'error': error,
    })


def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('view_appointment')


def about(request):
    return render(request, 'about.html', {
        'doctor_count': Doctor.objects.count(),
        'patient_count': Patient.objects.count(),
        'appointment_count': Appointment.objects.count(),
    })

def about(request):
    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()

    return render(request, 'about.html', {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
    })



from datetime import date

def Home(request):
    if not request.user.is_staff:
        return redirect('login')

    doctor_count = Doctor.objects.count()
    patient_count = Patient.objects.count()
    appointment_count = Appointment.objects.count()

    today_appointments = Appointment.objects.filter(date1=date.today())

    appoint = Appointment.objects.all().order_by('-id')[:5]

    context = {
        'doctor_count': doctor_count,
        'patient_count': patient_count,
        'appointment_count': appointment_count,
        'today_appointments': today_appointments,
        'appoint': appoint,
    }

    return render(request, 'index.html', context)