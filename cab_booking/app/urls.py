from django.urls import path
from . import views

  
urlpatterns=[
    path('',views.shop_login),
    path('shop_home',views.shop_home),
    path('logout/',views.e_shop_logout),
    path('add_cab',views.add_cabs,name='add_cab'),
    path('cab_list',views.cab_list,name='cab_list'),

    path('edit_cab/<pid>',views.edit_cabs),
    path('delete_cab/<pid>',views.delete_cabs),
    path('view_bookings/', views.view_bookings),


    



####################################

    path('user_home',views.user_home),
    path('register/',views.Register),
    path('contact/', views.contact, name='contact'),  
    path('about/',views.about),
    path('services/',views.services),
    path('view_cabs/<pid>',views.view_cabs),
    path('tariff/',views.tariff),
    path('vehicles/', views.vehicle_rentals),
    path('view_book/', views.view_book, name='view_book'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    # path('book_vehicle/<int:pid>/', views.book_form),
    path('book_form/<pid>/',views. book_form),
   
    path('book_now/<pid>', views.book_now),
 
    # path('book_now/<int:pid>/', views.book_now),  # Vehicle selected by 'pid'
    path('submit_booknow/',views. submit_booknow),



    







]