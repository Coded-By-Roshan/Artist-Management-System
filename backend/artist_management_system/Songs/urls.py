from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('view_songs/<int:artist_id>',views.view_songs,name='view_songs'),
        path('add_songs/<int:artist_id>',views.add_songs,name='add_songs'),
        path('edit_songs/',views.edit_song,name='edit_songs'),
        path('delete_song/<int:song_id>/<int:artist_id>',views.delete_song,name='delete_song'),

]
