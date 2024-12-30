from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from django.contrib.auth.models import User

# Create your views here.

def shop_login(request):
    if 'admin' in request.session:
        return redirect(shop_home)
    if 'user' in request.session:
        return redirect(user_home)
    if request.method=='POST':
        uname=request.POST['uname']
        password=request.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            login(request,data)
            if data.is_superuser:
                request.session['admin']=uname
                return redirect(shop_home)
            else:
                request.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(request, "invalid password")
            return redirect(shop_login)
    else:
        return render(request,'login.html')

def shop_home(req):
    cabs=Cab.objects.all()
    return render(req,'admin/home.html',{'Cab':cabs})



def add_cabs(req) :
    if 'admin' in req.session:
        if req.method=='POST':
            
            number_plate=req.POST['number_plate']
            model=req.POST['model']
            driver_name=req.POST['driver_name']
            available=req.POST['available']
            file=req.FILES['img']
            data=Cab.objects.create(number_plate=number_plate,model=model,driver_name=driver_name,available=available,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'admin/add_cab.html')
    else:
        return redirect(shop_login) 


def user_home(req):
    if 'user' in req.session:
        data=Cab.objects.all()
    cabs=Cab.objects.all()
    return render(req,'user/home.html',{'Cab':cabs})


def Register(req):
    if req.method=='POST':
        username=req.POST['uname']
        email=req.POST['email']
        password=req.POST['pswd']
        
        try:
            data=User.objects.create_user(first_name=username,email=email,username=email,password=password)
            data.save()
        except:
            messages.warning(req,"username already exist")
            return redirect(Register)
        return redirect(shop_login)
    else:
        return render(req,'user/Register.html')
    
def e_shop_logout(req):
    logout(req)
    req.session.flush()
    return redirect(shop_login)

def contact(req):
    return render(req,'user/contact.html')
def about(req):
    return render(req,'user/about.html')
def services(req):
    return render(req,'user/services.html')
def tariff(req):
    return render(req,'user/tariff.html')


