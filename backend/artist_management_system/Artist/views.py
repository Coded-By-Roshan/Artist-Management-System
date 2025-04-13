from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from .database import create_artist_table
from django.contrib import messages
from django.core.paginator import Paginator
import datetime,re
from django.urls import reverse
from AdminUser.decorators import login_required
import csv
from django.http import HttpResponse
from io import TextIOWrapper



def validate_artist_data(request, name, dob, gender, address, first_release_year):
    if not name or not re.match(r'^[A-Za-z\s]+$', name):
        messages.warning(request, 'Special Characters are not allowed in name.')
        return False

    if not dob:
        messages.warning(request, 'Date of birth is required.')
        return False

    if gender not in ['M', 'F', 'O']:
        messages.warning(request, 'Invalid gender selection.')
        return False

    if not address:
        messages.warning(request, 'Address is required.')
        return False

    current_year = datetime.date.today().year
    if int(first_release_year) > current_year:
        messages.warning(request, 'Release year must be a valid year.')
        return False
 
    return True


@login_required
def add_artist(request):
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
    create_artist_table()
    query = "SELECT * FROM Artist ORDER BY id DESC"
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
        messages.warning(request, f"Error deleting Artist: {e}")
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


@login_required
def import_artist(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
        reader = csv.DictReader(csv_file)
        
        success_count = 0

        with connection.cursor() as cursor:
            for row in reader:
                name = row['Name']
                dob = row['DOB']
                gender = row['Gender']
                address = row['Address']
                first_release_year = row['First Release Year']
                no_of_albums_released = row.get('Albums Released', 0)

                if not validate_artist_data(request, name, dob, gender, address, first_release_year):
                    continue

                cursor.execute("""
                    INSERT INTO Artist 
                    (name, dob, gender, address, first_release_year, no_of_albums_released, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    name, dob, gender, address, first_release_year,
                    no_of_albums_released, timezone.now(), timezone.now()
                ])
                success_count += 1
    
        messages.success(request, f"{success_count} artist(s) imported successfully.")
        return redirect(f"{reverse('dashboard')}#artistTab")

    messages.warning(request, 'Please upload a valid CSV file.')
    return redirect(f"{reverse('dashboard')}#artistTab")



@login_required
def export_artist(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name, dob, gender, address, first_release_year, no_of_albums_released,created_at,updated_at FROM Artist")
        artists = cursor.fetchall()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="artists.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'DOB', 'Gender', 'Address', 'First Release Year', 'Albums Released','Created','Updated'])
    for artist in artists:
        formatted_row = list(artist)
        for i in [6, 7]:
            if isinstance(formatted_row[i], (datetime.datetime, datetime.date)):
                local_dt = timezone.localtime(formatted_row[i])
                formatted_row[i] = local_dt.strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow(formatted_row)
    return response