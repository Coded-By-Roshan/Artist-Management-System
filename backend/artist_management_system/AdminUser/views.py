from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db import connection
import datetime
from .decorators import login_required
from django.contrib.auth.hashers import check_password
from .database import create_user_table
from Artist.views import get_artist
import re
from django.utils import timezone


@login_required
def dashboard(request):
    create_user_table()
    query = "SELECT * FROM Users ORDER BY id DESC"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    users = []
    for row in rows:
        users.append({
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'email': row[3],
            'phone': row[5],
            'dob': row[6],
            'gender': row[7],
            'address': row[8],
            'created_at': row[9],
            'updated_at':row[10]
        })
    user_paginator = Paginator(users, 2)  
    user_page_number = request.GET.get('page')
    user_page_obj = user_paginator.get_page(user_page_number)

    params = {'title': 'Dashboard','users': user_page_obj,'artists':get_artist(request)}
    return render(request, 'dashboard.html', params)


def validate_user_data(request, first_name, last_name, email, password, password_confirm, phone, dob, gender, address):
    if not all([first_name, last_name, email, password, password_confirm, phone, dob, gender, address]):
        messages.warning(request, 'All fields are required.')
        return False
    if (len(phone) != 10 or not phone.isdigit()):
        messages.warning(request, 'Wrong Phone Number.')
        return False
    if password != password_confirm:
        messages.warning(request, 'Passwords do not match.')
        return False
    if gender not in ['M', 'F', 'O']:
        messages.warning(request, 'Invalid gender selection.')
        return False
    if len(password) < 8:
        messages.warning(request, 'Password must be at least 8 characters long.')
        return False
    if not re.match(r'^[A-Za-z\s]+$', first_name):
        messages.warning(request, 'First name cannot contain special characters.')
        return False
    if not re.match(r'^[A-Za-z\s]+$', last_name):
        messages.warning(request, 'Last name cannot contain special characters.')
        return False
    return True


def register_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('conf_password') 
        error_list = {}
        username_required = False
        if not username:
            username_required = True
        if not email:
            error_list["username"] = True
        if not password:
            error_list["password"] = True
        if error_list:
            messages.warning(request,error_list)
        # if not password:
        #     error_list.append("Password is required")
        # if not password_confirm:
        #     error_list.append("confirm password required")
        # if username_required:
        #     messages.warning(request,"Username required")
        #     return redirect('register')
        if error_list:  
            messages.warning(request,error_list)
            return redirect('register')
        # if not all([username, email, password, password_confirm]):
        #     messages.warning(request,'All fields are required.')
        #     return redirect('register')
        if password != password_confirm:
            messages.warning(request,'Passwords do not match.')
            return redirect('register')
        if len(password) < 8:
            messages.warning(request,'Password must be at least 8 characters long.')
            return redirect('register') 
        if not re.match(r'^[A-Za-z\s]+$', username):
            messages.warning(request, 'Username cannot contain special characters.')
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
                messages.warning(request, 'Email already exists.')
            else:
                messages.warning(request, f'An error occurred during registration.')
            return redirect('register')
    return redirect('register')

def register(request):
    if request.session.get('user_id'):  
        return redirect('dashboard')
    params = {'title':'Register'}
    return render(request,'register.html',params)

def login_page(request):
    if request.session.get('user_id'):  
        return redirect('dashboard')
    params = {'title':'Login'}
    return render(request,'login.html',params)

def check_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not email or not password:
            messages.warning(request, 'Email and password are required.')
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
                return redirect('dashboard')
            else:
                messages.warning(request, 'Invalid password.')
        else:
            messages.warning(request, 'User does not exist.')
        return redirect('login_page')
    return redirect('login_page')

@login_required
def add_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('con_password')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')  
        if not validate_user_data(request, first_name, last_name, email, password, password_confirm, phone, dob, gender, address):
            return redirect('dashboard')
        
        query = """
            INSERT INTO Users (
                first_name, last_name, email, password, phone, dob, gender, address, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            first_name,
            last_name,
            email,
            make_password(password),  
            phone,
            dob,
            gender,
            address,
            timezone.now(),
            timezone.now(),
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            messages.success(request, 'Used added successfully')
            return redirect('dashboard')
        except Exception as e:
            if 'unique' in str(e).lower():
                messages.warning(request, 'Email already exists.')
            else:
                messages.warning(request, f'An error occurred during registration.{e}')
            return redirect('dashboard')
    return redirect('dashboard')

def logout_user(request):
    if 'user_id' in request.session:
        del request.session['user_id']
        messages.success(request, 'You have been logged out.')
    return redirect('login_page')

@login_required
def delete_user(request, user_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Users WHERE id = %s", [user_id])
        messages.success(request, "User deleted successfully.")
    except Exception as e:
        messages.warning(request, f"Error deleting user: {e}")
    return redirect('dashboard')

@login_required
def edit_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        if not validate_user_data(request, first_name, last_name, email, "password", "password", phone, dob, gender, address):
            return redirect('dashboard')
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Users WHERE id = %s", [user_id])
            user = cursor.fetchone()
            

        if not user:
            messages.warning(request, "User not found.")
            return redirect('dashboard')
        
        query = """
            UPDATE Users SET 
                first_name=%s, last_name=%s, email=%s, phone=%s,
                dob=%s, gender=%s, address=%s, updated_at=%s
            WHERE id=%s
        """
        params = [
            first_name, last_name, email, phone,
            dob, gender, address, datetime.datetime.now(), user_id
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
            messages.success(request, "User updated successfully.")
            return redirect('dashboard')
        except Exception as e:
            messages.warning(request, f"Error updating user: {e}")
            return redirect('edit_user', user_id=user_id)
    return redirect('dashboard')

