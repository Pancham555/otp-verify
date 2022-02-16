import random
# from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib.auth.models import User
from emailauth.functions import sendemail

name=''
email=''
password=''

def index(req):
    if(req.COOKIES.get('useremail')):
        return render(req, 'index.html')
    else:
        return redirect('/emailverify/')

def emailverify(req):
    if(req.method == 'GET'):
        return render(req, 'signup.html')
    else:   
        global name,email,password
        otp=random.randint(1000,9999)
        name = req.POST.get('name')
        email = req.POST.get('email')
        password = req.POST.get('password')
        sendemail(otp,email,settings.EMAIL_HOST_USER)
        responsedata=render(req, 'confirm.html',{'email':email})
        responsedata.set_cookie('otp', otp)
        name=name
        email=email
        password=password
        return responsedata


def createUser(req):
    global name,email,password
    otp=req.COOKIES.get('otp')
    getotp=int(req.POST.get('1'))*1000+int(req.POST.get('2'))*100+int(req.POST.get('3'))*10+int(req.POST.get('4'))
    if(int(otp) == getotp):
        try:
            user = User.objects.create_user(
                username=name, email=email, password=password)
            user.save()
            responsedata=render(req, 'confirmdone.html',{'name':name})
            responsedata.set_cookie('useremail', email,max_age=60*60*24*7)
            return responsedata
        except:
            return redirect('/emailverify/')
    else:
        return redirect('/emailverify/')

def resendotp(req):
    global email
    if(req.method == 'GET'):
        return render(req, 'confirm.html',{'email':email})
    otp=random.randint(1000,9999)
    sendemail(otp,email,settings.EMAIL_HOST_USER)
    responsedata=render(req, 'confirm.html',{'email':email})
    responsedata.set_cookie('otp', otp)
    return responsedata