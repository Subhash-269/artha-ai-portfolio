# Authentication System Setup Guide

## Overview
This project now includes a complete authentication system with:
- User registration (signup)
- User login
- Token-based authentication
- Protected routes
- Logout functionality

## Backend Setup

### 1. Install Required Packages
```bash
pip install django-cors-headers
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Start Django Server
```bash
python manage.py runserver
```

The backend will run on `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies
```bash
cd front_end
npm install
```

This will install `react-router-dom` and other required packages.

### 2. Start React Development Server
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## API Endpoints

### Authentication Endpoints:
- `POST /api/auth/signup/` - Register a new user
  - Body: `{ username, email, password, first_name (optional), last_name (optional) }`
  - Response: `{ token, user_id, username, email }`

- `POST /api/auth/login/` - Login user
  - Body: `{ username, password }`
  - Response: `{ token, user_id, username, email }`

- `POST /api/auth/logout/` - Logout user (requires authentication)
  - Headers: `Authorization: Token <your-token>`
  - Response: `{ message: "Successfully logged out" }`

- `GET /api/auth/user/` - Get current user info (requires authentication)
  - Headers: `Authorization: Token <your-token>`
  - Response: `{ user_id, username, email, first_name, last_name }`

## Features

### Frontend Components:
1. **Login Page** (`/login`)
   - Username and password fields
   - Redirect to signup page
   - Error handling
   - Responsive design

2. **Signup Page** (`/signup`)
   - Username, email, password fields
   - Optional first and last name
   - Password confirmation
   - Validation
   - Redirect to login page

3. **Dashboard** (`/dashboard`)
   - Protected route (requires authentication)
   - User welcome message
   - Logout button
   - Main portfolio application

### Security Features:
- Token-based authentication using Django Rest Framework
- CORS configuration for React frontend
- Protected routes on both frontend and backend
- Secure password validation
- Session management

## Usage Flow

1. **First Time User:**
   - Visit `/signup`
   - Create an account
   - Automatically logged in and redirected to dashboard

2. **Returning User:**
   - Visit `/login`
   - Enter credentials
   - Redirected to dashboard

3. **Protected Access:**
   - Token stored in localStorage
   - All API requests include authentication token
   - Automatic redirect to login if not authenticated

4. **Logout:**
   - Click logout button in navbar
   - Token deleted from server and localStorage
   - Redirected to login page

## File Structure

### Backend:
- `backend/auth_views.py` - Authentication view functions
- `backend/url.py` - URL routing including auth endpoints
- `portfolio/settings.py` - Django settings with CORS and REST framework config

### Frontend:
- `src/Login.js` - Login page component
- `src/Signup.js` - Signup page component
- `src/Dashboard.js` - Dashboard wrapper with navbar
- `src/AppRouter.js` - Main routing component
- `src/App.js` - Main portfolio application (DashboardDemo)

## Testing

### Create a Test User via Django Admin (Optional):
```bash
python manage.py createsuperuser
```

### Or Use the Signup Page:
1. Navigate to `http://localhost:3000/signup`
2. Fill in the form
3. Click "Sign Up"

## Troubleshooting

### CORS Errors:
- Ensure `django-cors-headers` is installed
- Check CORS settings in `portfolio/settings.py`
- Verify frontend is running on `http://localhost:3000`

### Authentication Errors:
- Check token is being sent in request headers
- Verify token exists in localStorage
- Check Django migrations are up to date

### Route Not Found:
- Ensure React Router is properly installed
- Check all routes are defined in `AppRouter.js`
- Verify navigation paths match route definitions
