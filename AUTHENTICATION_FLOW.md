# Authentication Flow Diagram

## User Journey

```
┌─────────────────────────────────────────────────────────────┐
│                    Visit http://localhost:3000               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Has Token?    │
                    └───────┬───────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
          NO  │                           │  YES
              │                           │
              ▼                           ▼
    ┌─────────────────┐         ┌─────────────────┐
    │  Login Page     │         │   Dashboard     │
    │  /login         │         │   /dashboard    │
    └────────┬────────┘         └─────────────────┘
             │
             │  Click "Sign up"
             │
             ▼
    ┌─────────────────┐
    │  Signup Page    │
    │  /signup        │
    └────────┬────────┘
             │
             │  Submit Form
             │
             ▼
    ┌─────────────────┐
    │  POST /api/auth/│
    │  signup/        │
    └────────┬────────┘
             │
             │  Returns Token
             │
             ▼
    ┌─────────────────┐
    │ Store Token &   │
    │ User in         │
    │ localStorage    │
    └────────┬────────┘
             │
             │  Auto Redirect
             │
             ▼
    ┌─────────────────┐
    │   Dashboard     │
    │   /dashboard    │
    └─────────────────┘
```

## Login Flow

```
┌─────────────────┐
│ User enters:    │
│ - Username      │
│ - Password      │
└────────┬────────┘
         │
         │ Submit
         │
         ▼
┌─────────────────┐
│ POST            │
│ /api/auth/login/│
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Django authenticates user   │
│ Creates/retrieves token     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Returns:                    │
│ - token                     │
│ - user_id                   │
│ - username                  │
│ - email                     │
│ - first_name, last_name     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ React stores:               │
│ localStorage.setItem(       │
│   'token', token            │
│ )                           │
│ localStorage.setItem(       │
│   'user', JSON.stringify({  │
│     id, username, email...  │
│   })                        │
│ )                           │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐
│ Navigate to     │
│ /dashboard      │
└─────────────────┘
```

## Protected API Request Flow

```
┌─────────────────┐
│ User on         │
│ Dashboard       │
└────────┬────────┘
         │
         │ Makes API request
         │
         ▼
┌─────────────────────────────┐
│ Fetch with headers:         │
│ Authorization: Token <xxx>  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Django REST Framework       │
│ validates token             │
└────────┬────────────────────┘
         │
    ┌────┴────┐
    │         │
Valid│      Invalid
    │         │
    ▼         ▼
┌────────┐ ┌────────┐
│ Allow  │ │ 401    │
│ Access │ │ Error  │
└────────┘ └────────┘
```

## Logout Flow

```
┌─────────────────┐
│ User clicks     │
│ Logout button   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ POST /api/auth/logout/      │
│ Headers:                    │
│ Authorization: Token <xxx>  │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Django deletes token        │
│ from database               │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ React removes:              │
│ - localStorage token        │
│ - localStorage user         │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐
│ Navigate to     │
│ /login          │
└─────────────────┘
```

## Component Hierarchy

```
AppRouter
├── Routes
│   ├── /login → Login
│   │   └── Form → POST /api/auth/login/
│   │
│   ├── /signup → Signup
│   │   └── Form → POST /api/auth/signup/
│   │
│   ├── /dashboard → Dashboard (Protected)
│   │   ├── NavBar
│   │   │   ├── User Info (from localStorage)
│   │   │   └── Logout Button → POST /api/auth/logout/
│   │   │
│   │   └── DashboardDemo
│   │       └── [Your Portfolio App]
│   │
│   └── / → Redirect to /login or /dashboard
```

## Database Tables

```
┌─────────────────────┐
│ auth_user           │
├─────────────────────┤
│ id (PK)             │
│ username (unique)   │
│ email               │
│ password (hashed)   │
│ first_name          │
│ last_name           │
│ is_active           │
│ date_joined         │
└──────────┬──────────┘
           │
           │ One-to-One
           │
           ▼
┌─────────────────────┐
│ authtoken_token     │
├─────────────────────┤
│ key (PK)            │
│ user_id (FK)        │
│ created             │
└─────────────────────┘
```

## Token Lifecycle

```
1. User Signs Up
   └─> Token Created
       └─> Stored in DB (authtoken_token)
       └─> Sent to Client
           └─> Stored in localStorage

2. User Makes Requests
   └─> Token sent in Header
       └─> Django validates
           └─> Grants/Denies access

3. User Logs Out
   └─> Token Deleted from DB
       └─> Removed from localStorage
           └─> Future requests fail

4. User Logs In Again
   └─> Token Retrieved or Created
       └─> Process repeats from step 1
```

## Security Model

```
┌──────────────────────────────────────────┐
│           FRONTEND (React)               │
│  ┌────────────────────────────────────┐  │
│  │  localStorage                      │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │ token: "abc123..."           │  │  │
│  │  │ user: { id, username, ... }  │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────┬───────────────────────────┘
               │
               │ HTTPS
               │ Headers: Authorization: Token abc123...
               │
               ▼
┌──────────────────────────────────────────┐
│           BACKEND (Django)               │
│  ┌────────────────────────────────────┐  │
│  │  REST Framework                    │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │ TokenAuthentication          │  │  │
│  │  │ - Validates token            │  │  │
│  │  │ - Looks up user              │  │  │
│  │  │ - Attaches to request.user   │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Database                          │  │
│  │  ┌──────────────────────────────┐  │  │
│  │  │ authtoken_token              │  │  │
│  │  │ key: "abc123..."             │  │  │
│  │  │ user_id: 1                   │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```
