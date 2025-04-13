from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
import datetime
from django.db import connection
from AdminUser.decorators import login_required
from .database import create_music_table
from django.utils import timezone

@login_required
def view_songs(request, artist_id):
    create_music_table()
    artist_name = ""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM Artist WHERE id = %s", [artist_id])
            result = cursor.fetchone()
            if result:
                artist_name = result[0]
    except Exception as e:
        messages.warning(request, f"Error fetching artist name: {str(e)}")

    query = "SELECT * FROM Music WHERE artist_id = %s ORDER BY updated_at DESC"
    with connection.cursor() as cursor:
        cursor.execute(query, [artist_id])
        rows = cursor.fetchall()

    songs = []
    for row in rows:
        songs.append({
            'id': row[0],
            'title': row[1],
            'album_name': row[2],
            'genre': row[3],
            'created_at': row[4],
            'updated_at': row[5],
            'artist_id': row[6]
        })

    songs_paginator = Paginator(songs, 2)
    songs_page_number = request.GET.get('song_page')
    songs_page_obj = songs_paginator.get_page(songs_page_number)
    generes = ['rnb', 'country', 'classic', 'rock', 'jazz']
    params = {'songs': songs_page_obj,'artist_id': artist_id,'artist_name': artist_name,'generes':generes}
    return render(request, 'music.html', params)


def validate_song_data(request, title, album_name, genre, valid_genres):
    if not all([title, album_name, genre]):
        messages.warning(request, 'All fields are required.')
        return False

    if genre not in valid_genres:
        messages.warning(request, 'Invalid genre selected.')
        return False

    return True

@login_required
def add_songs(request,artist_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        album_name = request.POST.get('album_name')
        genre = request.POST.get('genre')
        created_at = updated_at =timezone.now()
        valid_genres = ['rnb', 'country', 'classic', 'rock', 'jazz']

        if not validate_song_data(request, title, album_name, genre, valid_genres):
            return redirect('view_songs', artist_id=artist_id)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Music (title, album_name, genre, created_at, updated_at, artist_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, [title, album_name, genre, created_at, updated_at, artist_id])
                cursor.execute("""
                    SELECT COUNT(DISTINCT album_name) 
                    FROM Music 
                    WHERE artist_id = %s
                """, [artist_id])
                album_count = cursor.fetchone()[0]
                cursor.execute("""
                    UPDATE Artist 
                    SET no_of_albums_released = %s 
                    WHERE id = %s
                """, [album_count, artist_id])
            messages.success(request, 'Song added successfully.')
        except Exception as e:
            messages.warning(request, f'Failed to add song: {str(e)}')
        return redirect('view_songs', artist_id=artist_id)

    return redirect('view_songs', artist_id=artist_id)

@login_required
def edit_song(request):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        artist_id = request.POST.get('artist_id')
        print(song_id,artist_id)
        title = request.POST.get('title')
        album_name = request.POST.get('album_name')
        genre = request.POST.get('genre')
        updated_at = timezone.now()
        valid_genres = ['rnb', 'country', 'classic', 'rock', 'jazz']
        if not validate_song_data(request, title, album_name, genre, valid_genres):
            return redirect('view_songs', artist_id=artist_id)

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE Music
                    SET title = %s,
                        album_name = %s,
                        genre = %s,
                        updated_at = %s
                    WHERE id = %s
                """, [title, album_name, genre, updated_at, song_id])
            messages.success(request, 'Song updated successfully.')
        except Exception as e:
            messages.warning(request, f'Failed to update song: {str(e)}')

        return redirect('view_songs', artist_id=artist_id)

    return redirect('dashboard')

@login_required
def delete_song(request, song_id,artist_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Music WHERE id = %s", [song_id])
        messages.success(request, "Music deleted successfully.")
    except Exception as e:
        messages.warning(request, f"Error deleting Music: {e}")
    return redirect('view_songs', artist_id=artist_id)