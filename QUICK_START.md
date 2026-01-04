# Quick Start Guide

## Start the Application

### Terminal 1 - Django Backend:
```bash
cd "c:\Users\subha\Desktop\Workspace\Personal\AI Portfolio 2026"
python manage.py runserver
```

### Terminal 2 - React Frontend:
```bash
cd "c:\Users\subha\Desktop\Workspace\Personal\AI Portfolio 2026\front_end"
npm start
```

## Access the Application

1. Open your browser and go to: `http://localhost:3000`
2. You will be redirected to the login page
3. Click "Sign up" to create a new account
4. Fill in the registration form and submit
5. You'll be automatically logged in and redirected to the dashboard

## Default URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Login Page**: http://localhost:3000/login
- **Signup Page**: http://localhost:3000/signup
- **Dashboard**: http://localhost:3000/dashboard

## Test the System

### Create Your First Account:
1. Go to http://localhost:3000/signup
2. Enter:
   - Username: `testuser`
   - Email: `test@example.com`
   - Password: `testpass123`
   - (Optional) First Name and Last Name
3. Click "Sign Up"
4. You should be logged in and see the portfolio dashboard

### Login with Existing Account:
1. Go to http://localhost:3000/login
2. Enter your username and password
3. Click "Sign In"
4. Access the dashboard

### Logout:
1. Click the "Logout" button in the top navigation bar
2. You'll be redirected to the login page

## What's Working

✅ User Registration (Signup)
✅ User Login
✅ Token-based Authentication
✅ Protected Routes
✅ User Session Management
✅ Logout Functionality
✅ Database Integration (SQLite)
✅ CORS Configuration
✅ Beautiful UI with Gradients
✅ Form Validation
✅ Error Handling
✅ Responsive Design

## Troubleshooting

**Issue**: "Network error" when signing up/logging in
- **Solution**: Make sure Django server is running on port 8000

**Issue**: "Module not found: Can't resolve 'react-router-dom'"
- **Solution**: Run `npm install` in the front_end directory

**Issue**: CORS errors in browser console
- **Solution**: Verify Django CORS settings are configured correctly

**Issue**: Token authentication not working
- **Solution**: Check that migrations have been run (`python manage.py migrate`)
