from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from .database import create_artist_table
from django.contrib import messages
from django.core.paginator import Paginator
import datetime,re
from django.urls import reverse
from AdminUser.decorators import login_required




def validate_artist_data(request, name, dob, gender, address, first_release_year):
    if not name or not re.match(r'^[A-Za-z\s]+$', name):
        messages.error(request, 'Special Characters are not allowed in name.')
        return False

    if not dob:
        messages.error(request, 'Date of birth is required.')
        return False

    if gender not in ['M', 'F', 'O']:
        messages.error(request, 'Invalid gender selection.')
        return False

    if not address:
        messages.error(request, 'Address is required.')
        return False

    current_year = datetime.date.today().year
    if int(first_release_year) > current_year:
        messages.error(request, 'Release year must be a valid year.')
        return False
 
    return True


@login_required
def add_artist(request):
    create_artist_table()
    if request.method == 'POST':
        name = request.POST.get('fullname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        first_release_year = request.POST.get('release_year')
        created_at = timezone.now()
        updated_at = timezone.now()
        if not validate_artist_data(request, name, dob, gender, address, first_release_year):
            return redirect(f'{reverse('dashboard')}#artistTab')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO Artist 
                (name, dob, gender, address, first_release_year, no_of_albums_released, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, [name, dob, gender, address, first_release_year, 0, created_at, updated_at])
        messages.success(request, 'Artist added successfully!')
        return redirect(f'{reverse('dashboard')}#artistTab')  

    return redirect(f'{reverse('dashboard')}#artistTab') 

@login_required
def get_artist(request):
    query = "SELECT * FROM Artist ORDER BY updated_at DESC"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    artists = []
    for row in rows:
        artists.append({
            'id': row[0],
            'name': row[1],
            'dob': row[2],
            'gender': row[3],
            'address': row[4],
            'first_release_year': row[5],
            'no_of_album_released': row[6],
            'created_at': row[7],
            'updated_at':row[8]
        })
    artist_paginator = Paginator(artists, 2)  
    artist_page_number = request.GET.get('artistpage')
    artist_page_obj = artist_paginator.get_page(artist_page_number)
    return artist_page_obj

@login_required
def delete_artist(request, artist_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Artist WHERE id = %s", [artist_id])
        messages.success(request, "Artist deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Artist: {e}")
    return redirect(f'{reverse('dashboard')}#artistTab')

@login_required
def edit_artist(request):
    if request.method == 'POST':
        artist_id = request.POST.get('artist_id')
        name = request.POST.get('fullname')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        first_release_year = request.POST.get('release_year')
        updated_at = timezone.now()

        if not validate_artist_data(request, name, dob, gender, address, first_release_year):
            return redirect(f'{reverse('dashboard')}#artistTab')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE Artist 
                SET name=%s, dob=%s, gender=%s, address=%s, 
                    first_release_year=%s, updated_at=%s
                WHERE id=%s
            """, [name, dob, gender, address, first_release_year, updated_at, artist_id])

        messages.success(request, 'Artist updated successfully!')
        return redirect(f'{reverse('dashboard')}#artistTab')

    return redirect('dashboard')