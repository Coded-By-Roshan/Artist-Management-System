import os
import django
from django.db import connection

def create_user_table():
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts_user (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(500) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                dob TIMESTAMP NOT NULL,
                gender CHAR(1) NOT NULL CHECK (gender IN ('m', 'f', 'o')),
                address VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
