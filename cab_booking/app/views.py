from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.utils.crypto import get_random_string
import os
from django.contrib.auth.models import User
import random
from datetime import datetime
# from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .models import Booking
from .models import Vehicle

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


# def booking_confirmation(request):
#     # Get the confirmation code from the query string in the URL
#     confirmation_code = request.GET.get('confirmation_code')

#     # Render the confirmation page with the confirmation code
#     return render(request, 'user/booking_confirmation.html', {'confirmation_code': confirmation_code})


def generate_confirmation_code(length=6):
    """Generate a random numeric confirmation code of a given length."""
    return ''.join(random.choices('0123456789', k=length))  # Generates a numeric code (e.g., 123456)
def book_now(request, pid=None):
    if pid is not None:
        vehicle = get_object_or_404(Cab, id=pid)  # Get the vehicle based on the id (pid)
    else:
        vehicle = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user = request.user  # Get the logged-in user (using Django's auth system)
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Generate a random confirmation code (8 characters long)
            confirmation_code = get_random_string(length=8)  # Generate a random string

            # Calculate the total_amount dynamically if needed, for now, assume 100
            total_amount = 100  # For simplicity, using a static amount here
            status = "Confirmed"  # Booking status can be dynamically set

            # Create and save the booking
            bookings = Booking.objects.create(
                user=user,
                vehicle=vehicle,
                start_date=start_date,
                end_date=end_date,
                confirmation_code=confirmation_code,
                total_amount=total_amount,
                status=status
            )
            bookings.save()  # Save the booking to the database

            # Prepare the context for rendering the confirmation page
            context = {
                'confirmation_code': confirmation_code,
                'user': user,
                'vehicle': vehicle,
                'start_date': start_date,
                'end_date': end_date,
                'total_amount': total_amount,
                'status': status,
                'vehicle_id': vehicle.id if vehicle else None,
            }

            # Render the confirmation page with the booking details
            return render(request, 'user/booknow.html', context)
    
    else:
        form = BookingForm()

        context = {
            'form': form,
            'vehicle': vehicle,
            'cab_id': vehicle.id if vehicle else None,
        }

        # Render the booking form if the method is GET
        return render(request, 'user/booknow.html', context)


def vehicle_rentals(request):
    vehicles = Vehicle.objects.all()  # Fetch all vehicle rental details
    return render(request, 'user/tariff.html', {'vehicles': vehicles})
def submit_booknow(request):
    if request.method == "POST":
        # Get the form data
        user_name = request.POST['user_name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        vehicle = request.POST['vehicle']
        total_amount = request.POST['total_amount']

        # Generate the confirmation code
        confirmation_code = generate_confirmation_code()  # Call the function to generate the code

        # Save the booking in the database
        booking = Booking(
            user_name=user_name,
            start_date=start_date,
            end_date=end_date,
            vehicle=vehicle,
            total_amount=total_amount,
            confirmation_code=confirmation_code,  # Store confirmation code in the database
        )
        booking.save()

        # Redirect to the confirmation page with the confirmation code in the URL
        return redirect(f"/booking_confirmation/?confirmation_code={confirmation_code}")
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

# def view_cabs(req,pid):
#     if req.method == 'POST':
#         form = BookingForm(req.POST)
#         if form.is_valid():
#             user = User.objects.get(username=req.session['user'])  
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
            
#             confirmation_code = get_random_string(length=8)
#             total_amount = 100 
#             status = "Confirmed"

#             bookings = Booking(
#                 user=user, 
#                 start_date=start_date, 
#                 end_date=end_date, 
#                 confirmation_code=confirmation_code, 
#                 total_amount=total_amount, 
#                 status=status
#             )
#             bookings.save()
#             return redirect(book_now)
#         book=Booking.objects.all()
#         return render(req,'user/booknow.html',{'book_now':book})
#     bookings=Cab.objects.get(pk=pid)
#     return render(req,'user/view_cabs.html',{'Cab':bookings})
def view_cabs(request,pid):
    cabs = Cab.objects.all()  # Fetch all available cabs
    return render(request, 'user/view_cabs.html', {'cabs': cabs})



# def book_now(request, cab_id):
#     cab = Cab.objects.get(id=cab_id)  # Get the selected cab
#     confirmation_code = 45678

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             # Save the booking details
#             booking = form.save(commit=False)
#             booking.user = request.user  # Associate the booking with the logged-in user
#             booking.cab = cab  # Associate the booking with the selected cab
            
#             # Generate and assign the confirmation code
#             booking.confirmation_code = generate_confirmation_code()  # Dynamically generate a unique code
            
#             booking.save()

#             # Render the confirmation page
#             return render(request, 'book_now.html', {
#                 'confirmation_code': booking.confirmation_code,
#                 'user': request.user,
#                 'vehicle': cab,
#                 'start_date': booking.start_date,
#                 'end_date': booking.end_date,
#                 'total_amount': booking.total_amount,
#                 'status': booking.status,
#                 'Cab_id': cab.id,
#             })
#     else:
#         form = BookingForm()

#     # Render the form page for booking
#     return render(request, 'book_now.html', {
#         'form': form,
#         'Cab_id': cab.id,
#     })
def booking_confirmation(request):
    confirmation_code = generate_otp()  # Generate the confirmation code
    print(f"Generated OTP: {confirmation_code}")  # Debugging line, check in the console
    
    # If you want to render the confirmation page with the OTP
    return render(request, 'user/booking_confirmation.html', {'confirmation_code': confirmation_code})
# @login_required
# def view_bookings(request):
#     # Check if the method is POST (for creating a booking)
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
        
#         if form.is_valid():
#             # Use request.user instead of session data
#             user = request.user
            
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             confirmation_code = get_random_string(length=8)
#             total_amount = 100  # Assuming a static amount for simplicity
#             status = "Confirmed"

#             # Create the booking instance
#             booking = Booking(
#                 user=user, 
#                 start_date=start_date, 
#                 end_date=end_date, 
#                 confirmation_code=confirmation_code, 
#                 total_amount=total_amount, 
#                 status=status
#             )
#             booking.save()

#             # Redirect to another page after successful booking
#             return redirect('shop_home')  # Change 'shop_home' to your actual URL name

#     else:
#         form = BookingForm()  # Initialize the form for GET requests

#     # Fetch all bookings for the logged-in user
#     bookings = Booking.objects.filter(user=request.user)

#     # Pass the bookings and form to the template
#     return render(request, 'admin/view_bookings.html', {
#         'bookings': bookings,
       
#     })
@staff_member_required  # Ensure only admin users (staff) can access this view
def view_bookings(request):
    # Fetch all bookings in the system
    bookings = Booking.objects.all()  # All bookings, regardless of user
    
    return render(request, 'admin/view_bookings.html', {'bookings': bookings})