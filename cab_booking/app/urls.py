from django.urls import path
from . import views

  
urlpatterns=[
    path('',views.shop_login),
    path('shop_home',views.shop_home),
    path('logout',views.e_shop_logout),
    path('add_cab',views.add_cabs),

    



####################################

    path('user_home',views.user_home),
    path('register/',views.Register),
    path('contact',views.contact),
    path('about',views.about),
    path('services',views.services),
    path('tariff',views.tariff),



]