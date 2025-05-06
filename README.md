# simple_loginform_with_OTP
# Flask Authentication System with Email OTP Verification  A secure Flask web application implementing user authentication with email verification using OTP (One-Time Password). 


## Features

- User registration with email verification
- Secure password hashing
- Email OTP verification
- User login/logout functionality
- Protected dashboard route
- Input validation
- Flash messages for user feedback
- Responsive UI design



## Prerequisites

- Python 3.x
- Flask
- SQLite database
- SMTP server access (Gmail)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd login-form-with-OTP
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Configure email settings:
   - Open `utils/email.py`
   - Update `EMAIL_ADDRESS` with your Gmail address
   - Update `EMAIL_PASSWORD` with your Gmail app password

## Database Setup

The application automatically creates the SQLite database on first run. No manual setup required.

## Running the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Project Structure

```
├── app.py                 # Main application file
├── models/
│   └── user.py           # User model
├── routes/
│   └── auth.py           # Authentication routes
├── templates/            # HTML templates
│   ├── 404.html
│   ├── 500.html
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   └── verify.html
├── utils/
│   ├── email.py         # Email utilities
│   └── security.py      # Password hashing utilities
└── requirements.txt     # Project dependencies
```

## Security Features

- Password hashing using Werkzeug Security
- Session-based authentication
- Email verification
- Input validation and sanitization
- CSRF protection (Flask-WTF)
- Error handling pages

