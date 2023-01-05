from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import *
from main.models import *
from django.conf import settings
import sweetify
import random as r
import smtplib



def landingpage(request):
    if votingschedule.objects.filter(department='CEIT').exists():
        ceit = votingschedule.objects.get(department='CEIT') 
    else:
        ceit = 'No Schedule'

    if votingschedule.objects.filter(department='CTE').exists():
        cte = votingschedule.objects.get(department='CTE') 
    else:
        cte = 'No Schedule'

    if votingschedule.objects.filter(department='CAS').exists():
        cas = votingschedule.objects.get(department='CAS') 
    else:
        cas = 'No Schedule'

    if votingschedule.objects.filter(department='COT').exists():
        cot = votingschedule.objects.get(department='COT') 
    else:
        cot = 'No Schedule'
    if votingschedule.objects.filter(department='Main').exists():
        main = votingschedule.objects.get(department='Main') 
    else:
        main = 'No Schedule'
    if votingschedule.objects.all().exists():
        schedules = votingschedule.objects.all()
    else:
        schedules = []
    context = {
        'ceit': ceit,
        'cte': cte,
        'cas': cas,
        'cot': cot,
        'main': main,
        'today': datetime.date.today(),
        'schedules': schedules
    }
    return render(request, 'account/landingpage.html', context)


def generate_otp():
    otp = ""
    for i in range(r.randint(5, 8)):
        otp += str(r.randint(1, 9))
    return otp


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            if settings.OTP:
                login(request, user)
                if user.verified:
                    sweetify.success(request, 'Login Successfully')
                    return HttpResponseRedirect(reverse('home'))
                elif user.is_superuser:
                    sweetify.success(request, 'Login Successfully')
                    return HttpResponseRedirect(reverse('dashboard'))
                elif not user.verified:
                    login(request, user)
                    user = request.user
                    otp = generate_otp()
                    user.otp = otp
                    user.save()
                    try:
                        SENDER_EMAIL = settings.OTP_EMAIL
                        SENDER_PASSWORD = settings.OTP_PASSWORD
                        SUBJECT = "OTP Verification"
                        TEXT = otp
                        MESSAGE = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
                        RECEIVER_EMAIL = email
                        SERVER = smtplib.SMTP('smtp.gmail.com', 587)
                        SERVER.starttls()
                        SERVER.login(SENDER_EMAIL, SENDER_PASSWORD)
                        SERVER.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE)
                    except:
                        return HttpResponseRedirect(reverse('verify'))
                    sweetify.success(request, 'Check your email for verification')
                    return HttpResponseRedirect(reverse('verify'))
            else:
                #Bypass OTP
                login(request, user)
                user = request.user
                user.verified = True
                Receipt.objects.create(owner=user, department="Main Branch")
                Receipt.objects.create(owner=user, department=user.department)
                user.save()
                sweetify.success(request, 'Login Successfully')
                return HttpResponseRedirect(reverse('home'))
        else:
            sweetify.error(request, 'Invalid Credentials')
            return render(request, 'account/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'account/login.html')


def verify(request):
    otp_form = VerificationForm()
    context = {
        'otp_form': otp_form
    }
    if request.method == 'POST':
        user = request.user
        otp_form = VerificationForm(request.POST)
        user_otp = request.POST['otp']
        otp = int(user_otp)
        if otp == user.otp:
            user = request.user
            user.verified = True
            Receipt.objects.create(owner=user, department=user.department)
            Receipt.objects.create(owner=user, department='Main Branch')
            user.save()
            sweetify.success(request, 'Login Successfully')
            return HttpResponseRedirect(reverse('home'))
        else:
            print("failed")
            return render(request, 'account/verify.html', {'error': 'OTP is incorrect!', 'otp_form': otp_form})

    return render(request, 'account/verify.html', context)


def register_view(request):
    Registration_Form = RegistrationForm()
    if request.method == 'POST':
        Registration_Form = RegistrationForm(request.POST)
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 != password2:
            sweetify.error(request, 'Password do not match!')
            return render(request, 'account/register.html', {'error': 'Password do not match!', 'Registration_Form':Registration_Form})
        elif Registration_Form.is_valid():
            Registration_Form.save()
            sweetify.success(request, 'Registration Successful')
            return HttpResponseRedirect(reverse('login'))
        elif Account.objects.filter(email=email).exists():
            sweetify.error(request, 'Email already exist!')
            return render(request, 'account/register.html', {'error': 'Email already exist!','Registration_Form':Registration_Form})
        else:
            sweetify.error(request, 'Invalid Credentials')
            return render(request, 'account/register.html', {'error': 'Invalid Credentials','Registration_Form':Registration_Form})
    return render(request, 'account/register.html', {'Registration_Form':Registration_Form})


def logout_view(request):
    logout(request)
    return render(request, 'account/login.html')

