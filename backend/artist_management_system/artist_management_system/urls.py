from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('AdminUser.urls')),
    path('artist/',include('Artist.urls')),
    path('songs/',include('Songs.urls')),

]
