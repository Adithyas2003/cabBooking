from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


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

def generate_otp():
    return str(random.randint(100000, 999999))

def shop_login(request):
    if 'admin' in request.session:
        return redirect('shop_home')
    if 'user' in request.session:
        return redirect('user_home')

    if request.method == 'POST':
        uname = request.POST['uname']
        password = request.POST['password']
        user = authenticate(username=uname, password=password)  # Authenticate User

        if user:
            # ✅ If the user is an admin, log them in directly (NO OTP)
            if user.is_superuser:
                login(request, user)  # Direct login for admin
                request.session['admin'] = uname  # Store admin in session
                return redirect('shop_home')  # Redirect admin to shop_home

            # ✅ If the user is NOT an admin, require OTP verification
            else:
                otp = generate_otp()  # Generate OTP
                request.session['otp'] = otp  # Store OTP in session
                request.session['uname'] = uname  # Store username in session

                # Send OTP to the User's email
                send_mail(
                    'Your OTP for Login',
                    f'Your OTP is {otp}. Please enter it to complete your login.',
                    'your_email@example.com',  # Replace with sender email
                    [user.email],  # Receiver's email
                    fail_silently=False,
                )

                return redirect('verify_otp')  # Redirect to OTP verification page

        else:
            messages.warning(request, "Invalid username or password")
            return redirect('shop_login')

    return render(request, 'login.html')

def verify_otp(request):
    uname = request.session.get('uname')
    stored_otp = request.session.get('otp')

    # Check if session expired or missing values
    if not uname or not stored_otp:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('shop_login')

    if request.method == "POST":
        # Handle OTP Resend
        if "resend_otp" in request.POST:
            try:
                user = User.objects.get(username=uname)
                new_otp = generate_otp()
                request.session['otp'] = new_otp  # Store new OTP in session

                # Send new OTP email
                send_mail(
                    'Your New OTP',
                    f'Your new OTP is {new_otp}. Please enter it to verify your login.',
                    'your_email@example.com',  # Replace with sender email
                    [user.email],
                    fail_silently=False,
                )

                messages.success(request, "A new OTP has been sent to your email.")
                return redirect('verify_otp')

            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('shop_login')

        # ✅ Get entered OTP safely
        entered_otp = request.POST.get('otp', '')

        # ✅ Verify OTP
        if entered_otp == stored_otp:
            try:
                user = User.objects.get(username=uname)

                # ✅ If user is admin, deny OTP-based login (should never reach here)
                if user.is_superuser:
                    messages.error(request, "Admins do not require OTP verification.")
                    return redirect('shop_login')

                login(request, user)  # ✅ Log in the normal user

                # ✅ Clear OTP from session after successful login
                del request.session['otp']
                request.session['user'] = uname  # Store user in session

                return redirect('user_home')  # ✅ Redirect normal user to user_home

            except User.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('shop_login')

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')

    return render(request, 'user/verify_otp.html')
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
            seats = int(req.POST['seats'])  # Get seat selection

            price=req.POST['price']
            file=req.FILES['img']
            data=Cab.objects.create(number_plate=number_plate,model=model,driver_name=driver_name,available=available,seats=seats,price=price,img=file)
            
            data.save()
            return redirect(cab_list)
        else:
            return render(req,'admin/add_cab.html')
    else:
        return redirect(shop_login) 
def cab_list(request):
    six_seaters = Cab.objects.filter(seats=6)  
    twelve_seaters = Cab.objects.filter(seats=12)  
    fifteen_seaters = Cab.objects.filter(seats=15)  
    thirty_seaters = Cab.objects.filter(seats=30)  

    context = {
        'six_seaters': six_seaters,
        'twelve_seaters': twelve_seaters,
        'fifteen_seaters': fifteen_seaters,
        'thirty_seaters': thirty_seaters,
    }
    
    return render(request, 'user/cab_list.html', context)



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

def contact(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email_address = request.POST.get('email_address')
        message = request.POST.get('message')

        if not full_name or not email_address or not message:
            messages.error(request, "All fields are required.")
        else:
            Contact.objects.create(full_name=full_name, email_address=email_address, message=message)
            messages.success(request, "Your message has been sent successfully!")

            return redirect('contact')  

    return render(request, 'user/contact.html') 

def delete_booking(request, booking_id):
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if the user is not authenticated

    booking = get_object_or_404(Booking, id=booking_id, user=request.user)  # Ensure the booking belongs to the logged-in user
    booking.delete()  # Delete the booking
    return redirect('view_book')

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
        location =request.POST['location']
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
        
        
        confirmation_code = generate_confirmation_code(length=8)
        print(f"Generated Confirmation Code: {confirmation_code}")
        
        # Create and save the booking record in the database
        booking = Booking.objects.create(
            user=user,
            name=name,
            phone_number=phone_number,
            address=address,
            location=location,
            start_date=start_date,
            end_date=end_date,
            vehicle=cab,
            confirmation_code=confirmation_code,
            total_amount=total_amount
        )
        booking.save()
        send_confirmation_email(user.email, confirmation_code)

        
        # Render the confirmation page with the generated confirmation code
        return render(request, 'user/booking_confirmation.html', {'confirmation_code': confirmation_code})
    
def view_book(request):
  
    if 'user' not in request.session:
      
        return render(request, 'user/login.html')  
    
    try:
       
        user = User.objects.get(username=request.session['user'])
    except User.DoesNotExist:
       
        return render(request, 'user/login.html')
    
    
    bookings = Booking.objects.filter(user=user).order_by('-start_date')
    
    return render(request, 'user/viewbook.html', {'bookings': bookings})

def send_confirmation_email(user_email, confirmation_code):
    subject = "Cab Booking Confirmation Code"
    message = f"Your booking is confirmed!\n\nYour confirmation code: {confirmation_code}"
    
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )

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