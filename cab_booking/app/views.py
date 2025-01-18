from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.utils.crypto import get_random_string
import os
import string
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




def generate_confirmation_code(length=8):
    """Generate a random alphanumeric confirmation code of a given length."""
    # Create a pool of uppercase and lowercase letters + digits
    characters = string.ascii_letters + string.digits
    # Randomly choose characters from the pool and join them into a string
    return ''.join(random.choices(characters, k=length))



# def confirmation_code = generate_confirmation_code(length=8)
#     print(confirmation_code)  
def book_now(request, pid=None):
    if pid is not None:
        vehicle = get_object_or_404(Cab, id=pid)  # Get the vehicle based on the id (pid)
    else:
        vehicle = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            user = request.user  # Get the logged-in user
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Generate a random confirmation code (6 digits long)
            confirmation_code = generate_confirmation_code(length=6)

            # Calculate the total_amount dynamically
            total_amount = 100  # Assuming 100 for simplicity
            status = "Confirmed"

            # Create a new Booking instance (don't save it yet)
            booking = Booking(
                user=user,
                vehicle=vehicle,
                start_date=start_date,
                end_date=end_date,
                confirmation_code=confirmation_code,
                total_amount=total_amount,
                status=status
            )
            
            # Save the booking to the database
            booking.save()

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

            # Render the confirmation page
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
        vehicle_id = request.POST['vehicle']  # This should be the ID of the vehicle
        total_amount = request.POST['total_amount']

        # Fetch the vehicle object based on the vehicle_id from the form
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        # Generate the confirmation code
        confirmation_code = generate_confirmation_code()  # Ensure this is the string-based code

        # Save the booking in the database
        bookings = Booking(
            user=user,  # Ensure this matches your model field
            start_date=start_date,
            end_date=end_date,
            vehicle=vehicle,  # Assign the actual Vehicle object
            total_amount=total_amount,
            confirmation_code=confirmation_code,  # Store confirmation code in the database
        )
        bookings.save()  # Save to the database

        # Redirect to the confirmation page with the confirmation code in the URL
        return redirect(f"/booking_confirmation/?confirmation_code={confirmation_code}")
    else:
        # If the method is not POST, render a form (optional, depending on your logic)
        return render(request, 'user/booknow.html')

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
    # Generate the confirmation code (OTP)
    confirmation_code = generate_confirmation_code(length=8)  # Generate an 8-character alphanumeric confirmation code
    
    print(f"Generated Confirmation Code: {confirmation_code}")  # Debugging line, check in the console
    
    # Render the confirmation page with the OTP (confirmation code)
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