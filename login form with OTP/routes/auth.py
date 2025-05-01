from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User, db
from utils.email import generate_otp, send_otp_email
import re

auth = Blueprint('auth', __name__)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    # Password must be at least 8 characters long and contain at least one number and one letter
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@auth.route('/')
def home():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            
            # Input validation
            if not email or not password:
                flash('Please fill in all fields', 'error')
                return redirect(url_for('auth.signup'))
                
            if not is_valid_email(email):
                flash('Please enter a valid email address', 'error')
                return redirect(url_for('auth.signup'))
                
            if not is_valid_password(password):
                flash('Password must be at least 8 characters long and contain at least one number and one letter', 'error')
                return redirect(url_for('auth.signup'))
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('Email already registered!', 'error')
                return redirect(url_for('auth.signup'))
            
            # Create new user
            new_user = User(email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            # Generate and send OTP
            otp = generate_otp()
            session['otp'] = otp
            session['email'] = email
            send_otp_email(email, otp)
            
            return redirect(url_for('auth.verify'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.signup'))
    
    return render_template('signup.html')

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if 'email' not in session:
        flash('Please sign up first', 'error')
        return redirect(url_for('auth.signup'))

    if request.method == 'POST':
        try:
            user_otp = request.form.get('otp', '').strip()
            if not user_otp:
                flash('Please enter the OTP', 'error')
                return redirect(url_for('auth.verify'))
                
            if user_otp == session.get('otp'):
                email = session.get('email')
                user = User.query.filter_by(email=email).first()
                if user:
                    user.is_verified = True
                    db.session.commit()
                    session.pop('otp', None)  # Clear OTP from session
                    flash('Email verified successfully!', 'success')
                    return redirect(url_for('auth.login'))
                else:
                    flash('User not found. Please sign up again.', 'error')
                    return redirect(url_for('auth.signup'))
            else:
                flash('Invalid OTP!', 'error')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.verify'))
    
    return render_template('verify.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('auth.home'))

    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            
            if not email or not password:
                flash('Please fill in all fields', 'error')
                return redirect(url_for('auth.login'))
                
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                if user.is_verified:
                    session['user_id'] = user.id
                    session.permanent = True
                    flash('Login successful!', 'success')
                    return redirect(url_for('auth.home'))
                else:
                    # Resend verification email
                    otp = generate_otp()
                    session['otp'] = otp
                    session['email'] = email
                    send_otp_email(email, otp)
                    flash('Please verify your email first. A new OTP has been sent.', 'error')
                    return redirect(url_for('auth.verify'))
            else:
                flash('Invalid email or password!', 'error')
        except Exception as e:
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('auth.login')) 