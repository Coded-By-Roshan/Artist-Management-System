from django.db import connection

def create_music_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Music (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            album_name VARCHAR(255) NOT NULL,
            genre CHAR(10) NOT NULL CHECK (genre IN ('rnb', 'country', 'classic', 'rock', 'jazz')),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            artist_id INTEGER NOT NULL,
            FOREIGN KEY (artist_id) REFERENCES Artist(id) ON DELETE CASCADE
        );
        """)

