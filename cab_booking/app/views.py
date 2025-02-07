from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.utils.crypto import get_random_string
import os
import string
from datetime import datetime
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
    # Fetch the vehicle if pid is provided
    vehicle = get_object_or_404(Cab, id=pid)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create the booking instance but don’t save yet
            booking = form.save(commit=False)
            booking.user = request.user  # Assign the logged-in user
            booking.vehicle = vehicle  # Assign the vehicle from pid
            
            # Generate a confirmation code (OTP or random code)
            confirmation_code = generate_otp()  # Ensure this function is defined
            booking.confirmation_code = confirmation_code  # Store the confirmation code

            # Save the booking to the database
            booking.save()

            # Redirect to the booking confirmation page
            return redirect('booking_confirmation', confirmation_code=booking.confirmation_code)

    else:
        form = BookingForm()

    return render(request, 'user/bookingform.html', {'form': form, 'vehicle': vehicle})




def generate_confirmation_code(length=8):
    """Generate a random alphanumeric confirmation code of a given length."""
    # Create a pool of uppercase and lowercase letters + digits
    characters = string.ascii_letters + string.digits
    # Randomly choose characters from the pool and join them into a string
    return ''.join(random.choices(characters, k=length))


# def book_now(request, pid=None):
    
#     vehicle = get_object_or_404(Cab, id=pid) if pid else None

#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
          
#             user = request.user
#             start_date = form.cleaned_data['start_date']
#             end_date = form.cleaned_data['end_date']
#             name = form.cleaned_data['name']
#             address = form.cleaned_data['address']
#             phone_number = form.cleaned_data['phone_number']
#             total_amount = form.cleaned_data['total_amount']
#             status = form.cleaned_data['status']
            
#             confirmation_code = form.cleaned_data.get('confirmation_code', None) or "CONFIRM-" + str(Booking.objects.count() + 1)
            
            
#             booking = Booking.objects.create(
#                 user=user,
#                 vehicle=vehicle,
#                 start_date=start_date,
#                 end_date=end_date,
#                 name=name,
#                 address=address,
#                 phone_number=phone_number,
#                 total_amount=total_amount,
#                 status=status,
#                 confirmation_code=confirmation_code  
#             )
#             booking.save()

            
#             context = {
#                 'booking': booking,
#                 'confirmation_code': booking.confirmation_code  
#             }

            
#             return render(request, 'user/booking_confirmation.html', context)

#         else:
            
#             return HttpResponse("Form is not valid. e form is not valid, display an error messagePlease check the fields.")
#     else:
#         form = BookingForm()

#     return render(request, 'user/booknow.html', {'form': form, 'vehicle': vehicle})


def vehicle_rentals(request):
    vehicles = Vehicle.objects.all()  
    return render(request, 'user/tariff.html', {'vehicles': vehicles})
def submit_booknow(request):
    if request.method == "POST":
        
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
    print(pid)
    return render(request, 'user/view_cabs.html', {'cabs': cabs,'pid':pid})
def generate_confirmation_code(length=8):
  
   
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def book_now(request, pid):
    cab = Cab.objects.get(pk=pid)  # Fetch the cab based on the given id (pid)
    user = User.objects.get(username=request.session['user'])  # Get the logged-in user
    
    if request.method == 'POST':
        # Collect form data
        name = request.POST['name']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        vehicle_type = request.POST['vehicle_type']
        
        # Extract price and days from the form data
        price = float(cab.price)  # Use the price of the cab from the model (assuming `price` field exists on the `Cab` model)
        days = int(request.POST.get('days', 0))  # Calculate the number of days (if days are provided in the form)

        # Calculate the total amount
                # Fetch the price of the cab (price per day)
        price = float(cab.price)  # Assuming 'price' is a field in the Cab model, which is the price per day
        
        # Calculate the number of days between the start date and end date
        date1 = datetime.strptime(start_date, "%Y-%m-%d").date()
        date2 = datetime.strptime(end_date, "%Y-%m-%d").date()
        date_diff = (date2 - date1).days  # Number of days between start and end date
        
        # Ensure the duration is valid (positive number of days)
        if date_diff <= 0:
            return render(request, 'user/error_page.html', {'error': "Invalid date range. End date must be after start date."})

        # Calculate the total amount (price per day * number of days)
        total_amount = price * date_diff
        
        # Print the calculated duration and total amount
        print(f"Duration in days: {date_diff} days, Total Amount: ${total_amount:.2f}")
        
        # Generate a confirmation code (assuming you have a function for this)
        confirmation_code = generate_confirmation_code(length=8)
        print(f"Generated Confirmation Code: {confirmation_code}")
        
        # Create and save the booking record in the database
        booking = Booking.objects.create(
            user=user,
            name=name,
            phone_number=phone_number,
            address=address,
            start_date=start_date,
            end_date=end_date,
            vehicle=cab,
            confirmation_code=confirmation_code,
            total_amount=total_amount
        )
        booking.save()
        
        # Render the confirmation page with the generated confirmation code
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
@staff_member_required  
def view_bookings(request):
    
    bookings = Booking.objects.all()  
    
    return render(request, 'admin/view_bookings.html', {'bookings': bookings})