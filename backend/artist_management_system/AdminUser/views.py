from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.db import connection
import datetime
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
import re
from .database import create_user_table


def base(request):
    return render(request,'base.html')

def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('con_password') 
        print(username, email, password, password_confirm)
        if not all([username, email, password, password_confirm]):
            messages.error(request,'All fields are required.')
            return redirect('register')
        if password != password_confirm:
            messages.error(request,'Passwords do not match.')
            return redirect('register')
        if len(password) < 8:
            messages.error(request,'Password must be at least 8 characters long.')
            return redirect('register')   
        try:
            password = make_password(password)
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO auth_user (
                        password, last_login, is_superuser,
                        username, first_name, last_name,
                        email, is_staff, is_active, date_joined
                    ) VALUES (%s, NULL, TRUE, %s, '', '', %s, TRUE, TRUE, datetime('now'))
                """, [password, username, email])

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login_page')
        except Exception as e:
            if 'unique' in str(e).lower():
                messages.error(request, 'Email already exists.')
            else:
                messages.error(request, f'An error occurred during registration.{e}')
            return redirect('register')
    return redirect('register')

def register(request):
    params = {'title':'Register'}
    return render(request,'register.html',params)

def login_page(request):
    params = {'title':'Login'}
    return render(request,'login.html',params)

def check_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'login.html')
        query = "SELECT id, password FROM auth_user WHERE email = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [email])
            result = cursor.fetchone()
        if result:
            user_id, hashed_password = result
            if check_password(password, hashed_password):
                request.session['user_id'] = user_id
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid password.')
        else:
            messages.error(request, 'User does not exist.')
        return redirect('login_page')
    return redirect('home')


