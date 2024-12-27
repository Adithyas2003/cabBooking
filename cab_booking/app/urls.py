from django.urls import path
from . import views

  
urlpatterns=[
    path('',views.e_shop_login),
    path('shop_home',views.shop_home),
    path('logout',views.e_shop_logout),
    



####################################

    path('user_home',views.user_home),
    path('register/',views.Register),
]