from django.urls import path
from . import views
from app.views import book_now

  
urlpatterns=[
    path('',views.shop_login),
    path('shop_home',views.shop_home),
    path('logout/',views.e_shop_logout),
    path('add_cab',views.add_cabs),
    path('edit_cab/<pid>',views.edit_cabs),
    path('delete_cab/<pid>',views.delete_cabs),
    path('view_bookings/', views.view_bookings),


    



####################################

    path('user_home',views.user_home),
    path('register/',views.Register),
    path('contact/',views.contact),
    path('about/',views.about),
    path('services/',views.services),
    path('view_cabs/<pid>',views.view_cabs),
    path('tariff/',views.tariff),
    path('vehicles/', views.vehicle_rentals, name='vehicle_rentals'),
    path('booking_confirmation/', views.booking_confirmation, name='booking_confirmation'),  # Confirmation page
    # path('book_vehicle/<int:pid>/', views.book_form),
    path('book_form/<pid>/',views. book_form),
   
    path('book_now/<pid>', views.book_now),
 
    # path('book_now/<int:pid>/', views.book_now, name='book_now_with_pid'),  # Vehicle selected by 'pid'
    path('submit_booknow/',views. submit_booknow),



    







]