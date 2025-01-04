from django.urls import path
from . import views

  
urlpatterns=[
    path('',views.shop_login),
    path('shop_home',views.shop_home),
    path('logout',views.e_shop_logout),
    path('add_cab',views.add_cabs),
    path('edit_cab/<pid>',views.edit_cabs),
    path('delete_cab/<pid>',views.delete_cabs),
    path('view_bookings/<pid>',views.delete_cabs),


    



####################################

    path('user_home',views.user_home),
    path('register/',views.Register),
    path('contact',views.contact),
    path('about',views.about),
    path('services',views.services),
    path('tariff',views.tariff),
    path(' booking_confirmation',views. booking_confirmation),
    # path('book_vehicle/<int:pid>/', views.book_form),
    path('book_form/<int:pid>/',views. book_form),
    path('book_now/',views. book_now),
    path('submit_booknow/',views. submit_booknow),



    







]