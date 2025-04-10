from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard, name="dashboard"),
    path('register/',views.register,name='register'),
    path('register_admin/',views.register_admin,name='register_admin'),
    path('login/',views.login_page,name='login_page'),
    path('check_login/',views.check_login,name='check_login'),
    path('logout/',views.logout_user,name="logout"),
    path('add_user/',views.add_user,name="add_user"),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),  
    path('edit_user/', views.edit_user, name='edit_user'),
]
