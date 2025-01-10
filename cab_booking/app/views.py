from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
import random
from datetime import datetime
from django.http import HttpResponse

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
            price=req.POST['price']
            file=req.FILES['img']
            data=Cab.objects.create(number_plate=number_plate,model=model,driver_name=driver_name,available=available,price=price,img=file)
            data.save()
            return redirect(shop_home)
        else:
            return render(req,'admin/add_cab.html')
    else:
        return redirect(shop_login) 

def edit_cabs(req,pid):
    if req.method=='POST':
         
            number_plate=req.POST['number_plate']
            model=req.POST['model']
            driver_name=req.POST['driver_name']
            available=req.POST['available']
            price=req.POST['price']
            file=req.FILES.get('img')
            if file:
                Cab.objects.filter(pk=pid).update(number_plate=number_plate,model=model,driver_name=driver_name,available=available,price=price)
                data=Cab.objects.get(pk=pid)
                data.img=file
                data.save()
            else:
                Cab.objects.filter(pk=pid).update(number_plate=number_plate,model=model,driver_name=driver_name,available=available,price=price)
                return redirect(shop_home)
    else:
        data=Cab.objects.get(pk=pid)
        return render(req,'admin/edit_cab.html',{'data':data})

def delete_cabs(req,pid):
    data=Cab.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)

# def cart_pro_buy(req,cid):
#     cart=cart.objects.get(pk=cid)
#     product=cart.Product
#     user=cart.user
#     qty=cart.qty
#     price=product.offer_price*qty
#     buy=Buy.objects.create(Product=product,user=user,qty=qty,price=price)
#     buy.save()
#     return redirect(bookings)

# def pro_buy(req,pid):
#     Products=Cab.objects.get(pk=pid)
#     user=User.objects.get(username=req.session['user'])
#     qty=1
#     price=Products.offer_price
#     buy=Buy.objects.create(Product=Products,user=user,qty=qty,price=price)
#     buy.save()
#     return redirect(bookings)


# def bookings(req):
#     user=User.objects.get(username=req.session['user'])
#     buy=Buy.objects.filter(user=user)[::-1]
#     return render(req,'user/bookings.html',{'bookings':buy})



# def book_form(request, pid):
   
#     vehicle = Cab.objects.get(id=pid)
    
#     if request.method == 'POST':
      
#         form = Booking(request.POST)
#         if form.is_valid():
#             booking = form.save(commit=False)
#             booking.user = request.user
#             booking.vehicle = vehicle
#             booking.save()

            
#             return redirect('booking_confirmation', confirmation_code=booking.confirmation_code)

#     else:
        
#         form = Booking(vehicle=vehicle)

#     return render(request, 'user/bookingform.html', {'form': form, 'vehicle': vehicle})


def generate_otp(length=6):
    otp = ''.join(random.choices('0123456789', k=length))  
    return otp

# Booking form view
def book_form(request, pid):
    vehicle = Cab.objects.get(id=pid)
    
    if request.method == 'POST':
        form = Booking(request.POST)
        if form.is_valid():
            
            Booking = form.save(commit=False)
            Booking.user = request.user
            Booking.vehicle = vehicle
            
           
            confirmation_code = generate_otp()
            Booking.confirmation_code = confirmation_code  
            Booking.save()

           
            return redirect('booking_confirmation', confirmation_code=Booking.confirmation_code)

    else:
        form = Booking(vehicle=vehicle)

    return render(request, 'user/bookingform.html', {'form': form, 'vehicle': vehicle})


def booking_confirmation(request):
    confirmation_code = generate_otp()  # Generate the confirmation code
    print(f"Generated OTP: {confirmation_code}")  # Debugging line, check in the console
    return render(request, 'user/booking_confirmation.html', {'confirmation_code': confirmation_code})


# def book_now(request):
#     return render(request, 'user/booknow.html')


# def pro_buy(req,pid):
#     product=Product.objects.get(pk=pid)
#     user=User.objects.get(username=req.session['user'])
#     qty=1
#     price=product.offer_price
#     buy=Buy.objects.create(Product=product,user=user,qty=qty,price=price)
#     buy.save()
#     return redirect(bookings)

def book_now(request):
    if request.method == "POST":
        
        user = request.POST.get('name')
        vehicle = request.POST.get('vehicle')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
      

        if not all([user, vehicle, start_date, end_date]):
            return HttpResponse("Please fill out all the fields.", status=400)

        confirmation_code = str(random.randint(100000, 999999))
        data=Booking.objects.create(user=user,vehicle=vehicle,start_date=start_date,end_date=end_date,total_amount=400,status='pending')
        data.save()
    else:
        print('data save')
       
        return render(request, 'user/booknow.html')
    product=Cab.objects.get(pk=id)
    user=User.objects.get(username=request.session['user'])
    start_date=21-10-2024
    end_date=22-10-24
    price=product.offer_price
    booking=Booking.objects.create(Product=product,user=user,start_date=start_date,end_date=end_date,price=price)
    booking.save()
    return redirect(book_now)

        # return render(request, 'user/booknow.html', {
        #     'confirmation_code': confirmation_code,
        #     'user': user,
        #     'vehicle': vehicle,
        #     'start_date': start_date,
        #     'end_date': end_date,
        #     'total_amount': total_amount,
        #     'status': status,
        # })

        

# def book_now(request):
#     if request.method == 'POST':
#         user = request.POST.get('name')
#         vehicle = request.POST.get('vehicle')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         # confirmation_code = request.POST.get('total_amount')
#         total_amount = request.POST.get('total_amount')
#         status = request.POST.get('status')


#         data = Booking(name=user,vehicle=vehicle,start_date=start_date,end_date=end_date,total_amount=total_amount,status=status)
#         data.save()

#         return redirect(book_now)

#     bookings = Booking.objects.all()

#     return render(request, 'user/booknow.html', {'book_now': bookings})





def submit_booknow(request):
    if request.method == 'POST':
        
        confirmation_code = generate_otp()

        return redirect('booking_confirmation', confirmation_code=Booking.confirmation_code)

    return render(request, 'user/submit_booknow.html/',)
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

def view_bookings(request):
    if request.method == "POST":
       
        user = request.POST.get('name')
        vehicle = request.POST.get('vehicle')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_amount = request.POST.get('total_amount')
        status = request.POST.get('status')
        if not all([user, vehicle, start_date, end_date, total_amount, status]):
            return HttpResponse("Please fill out all the fields.", status=400)
       
        confirmation_code = str(random.randint(100000, 999999))
        confirmation_code.save()

    bookings = Booking.objects.all()
    return render(request, 'admin/view_bookings.html', {'bookings': bookings})
