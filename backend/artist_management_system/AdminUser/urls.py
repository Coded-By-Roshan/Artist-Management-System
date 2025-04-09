from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.register,name='register'),
    path('register_admin/',views.register_admin,name='register_admin'),
    path('login/',views.login_page,name='login_page'),
    path('check_login/',views.check_login,name='check_login'),
    path('',views.base, name="home")
]
