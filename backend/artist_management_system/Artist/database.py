from django.db import connection

def create_artist_table():
    with connection.cursor() as cursor:
        cursor.execute("""
           CREATE TABLE IF NOT EXISTS Artist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                dob DATE NOT NULL,
                gender CHAR(1) NOT NULL CHECK (gender IN ('M', 'F', 'O')),
                address VARCHAR(255) NOT NULL,
                first_release_year INTEGER NOT NULL, 
                no_of_albums_released INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
