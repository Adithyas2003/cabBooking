from django.urls import path
from . import views

  
urlpatterns=[
    path('', views.shop_login, name='shop_login'),  # ✅ Login Page
    path('shop_home',views.shop_home,name='shop_home'),
    path('logout/',views.e_shop_logout, name='e_shop_logout'),
    path('add_cab',views.add_cabs,name='add_cab'),
    path('cab_list',views.cab_list,name='cab_list'),
    
    path('edit_cab/<pid>',views.edit_cabs),
    path('delete_cab/<pid>',views.delete_cabs),
    path('view_bookings/', views.view_bookings),


    



####################################

    path('user/home/', views.user_home, name='user_home'),  # Make sure this is correctly defined
    path('user/logout/',views.e_shop_logout),
    path('user/payment_success/',views.payment_success, name='payment_success'),
    path('register/',views.Register),
    path('user/contact/', views.contact, name='contact'),  
    path('user/about/',views.about),
    path('user/services/',views.services),
    path('user/home/view_cabs/<int:pid>/', views.view_cabs, name='view_cabs'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('user/vehicles/', views.vehicle_rentals),
    path('user/home/view_book/',views.view_book, name='view_book'),
    path('user/delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    # path('book_vehicle/<int:pid>/', views.book_form),
    path('user/book_form/<pid>/',views. book_form),
   
    # path('book_now/<int:pid>',views.book_now, name='book_now'),
    path('book_now/<int:pid>',views.demo, name='book_now'),
    
 
    # path('book_now/<int:pid>/', views.book_now),  # Vehicle selected by 'pid'
    path('user/submit_booknow/',views. submit_booknow),



    







]