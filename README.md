# Artist Management System 🎵

A simple Django-based Admin Panel to manage records of users, artists, and their song collections.

## 🚀 Project Summary

This application provides an admin dashboard where authenticated admin users can:
- Register and log in
- Manage users, artists, and songs
- Import/Export artist data in CSV format

## 🛠️ Tech Stack

- **Framework**: Django
- **Database**: SQLite
- **Frontend**: Django Templates,Javascript
- **Authentication**: Basic session-based login

## 📁 Database Schema

1. **User**  
2. **Artist**  
3. **Song**

All CRUD operations are to be performed using **raw SQL queries**, not Django ORM.

## 🔧 Features

### 🔐 Authentication
- Admin users can register and log in.
- Only logged-in users can access the dashboard.

### 📊 Dashboard (after login)
1. **User Management**
   - Paginated list view
   - Create, update, delete users

2. **Artist Management**
   - Paginated list view
   - Create, update, delete artists
   - Display total album of artist by counting unique albums from music table
   - CSV import/export functionality
   - Button to view songs for an artist

3. **Song Management**
   - List all songs for an artist
   - Create, update, delete songs

4. **Logout**
   - Log out from the session

### ✅ Validations
- All input fields are properly validated.
- Error messages are displayed on the forms.

## 🔄 CSV Support
- Export all artists into a CSV file.
- Import artists using a pre-defined CSV format.

## 🧰 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Coded-By-Roshan/Artist-Management-System.git
  

2. **Intall dependencies**

   ```bash
   cd backend/artist_management_system
   pip install -r requirements.txt


3. **Run server**

   ```bash
   python manage.py runserver


   

