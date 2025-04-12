from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("add_artist",views.add_artist,name='add_artist'),
    path("delete_artist/<int:artist_id>",views.delete_artist,name='delete_artist'),
    path("edit_artist",views.edit_artist,name='edit_artist'),
    path("import_artist",views.import_artist,name='import_artist'),
    path("export_artist",views.export_artist,name='export_artist'),

]
