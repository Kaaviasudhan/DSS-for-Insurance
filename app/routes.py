import signal
import sys
from flask import Flask
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import socket
from flask_mail import Mail, Message
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime
import os

from werkzeug.security import check_password_hash, generate_password_hash

from . import mongo, mail  # Import 'mail' from your '__init__.py'

# Create a Blueprint
main_bp = Blueprint('main', __name__)

# MongoDB Configuration
client = MongoClient(os.environ.get('MONGO_URI'))  # Get Mongo URI from .env
db = client['login_system']
users = db['users']  # Assuming 'users' is the collection name

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # Perform any cleanup here
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


# Decorator to restrict access based on user roles
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'email' not in session:
            flash('Please log in first.', 'danger')
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def role_required(role):
    def decorator(f):
        def wrapper(*args, **kwargs):
            user = users.find_one({"email": session['email']})
            if user and user['role'] != role:
                flash(f'Access denied for {role}s only.', 'danger')
                return redirect(url_for('main.dashboard'))
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Function to check if the system has internet connection
def check_internet_connection():
    try:
        # Check if we can resolve the host for internet connectivity
        socket.create_connection(("www.google.com", 80), 2)
        return True
    except OSError:
        return False

@main_bp.route('/')
def index():
    return render_template('guest/index.html')

@main_bp.route('/consultancy', methods=['POST'])
def consultancy():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Ensure mongo.db.consultancy is the correct collection
        mongo.db.consultancy.insert_one({
            'name': name,
            'email': email
        })
        
        return redirect(url_for('main.index'))
    
@main_bp.route('/about')
def about():
    return render_template('guest/about.html')

@main_bp.route('/insurance')
def insurance():
    return render_template('guest/insurance.html')

@main_bp.route('/news-Insurance')
def newsinsurance():
    return render_template('guest/news.html')

@main_bp.route('/contact')
def contact():
    return render_template('guest/contact.html')

# @main_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         user = users.find_one({"email": email})
        
#         if user and check_password_hash(user['password'], password):
#             session['email'] = email
#             session['role'] = user['role']
#             flash('Login successful!', 'success')
#             send_email(email, user['email'], "Login successful")
#             return redirect(url_for('main.dashboard'))
#         else:
#             flash('Invalid credentials, please try again.', 'danger')
#             send_email(email, email, "Login failed")
#             return redirect(url_for('main.login'))
    
#     return render_template('users/login.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check for internet connection before allowing login
        if not check_internet_connection():
            flash('No internet connection. Please check your network and try again.', 'danger')
            return redirect(url_for('main.login'))  # Prevent login and reload login page

        # Proceed with login process if internet is available
        email = request.form['email']
        password = request.form['password']
        
        user = users.find_one({"email": email})
        
        if user and check_password_hash(user['password'], password):
            session['email'] = email
            session['role'] = user['role']
            flash('Login successful!', 'success')
            send_email(email, user['email'], "Login successful")
            return redirect(url_for('main.introduction'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
            send_email(email, email, "Login failed")
            return redirect(url_for('main.login'))
    
    return render_template('users/login.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    role = session['role']
    return render_template('users/dashboard.html', role=role)

# Function to send emails
def send_email(to, username, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_body = f"""
    <p>Dear {username},</p>
    <p>Your login attempt was: <strong>{status}</strong></p>
    <p>Timestamp: {timestamp}</p>
    """
    
    msg = Message('Login Status', recipients=[to])
    msg.html = html_body
    mail.send(msg)

# Logout route
@main_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))

# Admin panel
# Admin dashboard to manage users
@main_bp.route('/admin_dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    all_users = users.find()

    # Query MongoDB to get user count and admin count
    user_count = mongo.db.users.count_documents({})  # Count all users
    admin_count = mongo.db.users.count_documents({"role": "admin"})  # Count all admins
    monthly_growth = 20  # Replace with actual calculation logic if needed

    return render_template('admin/admin_dashboard.html', users=all_users, user_count=user_count, 
                           admin_count=admin_count, monthly_growth=monthly_growth)

# User Mngts:

# Admin can create new users
@main_bp.route('/create_user', methods=['POST'])
@login_required
@role_required('admin')
def create_user():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # Check if the user already exists
    existing_user = mongo.db.users.find_one({'email': email})

    if existing_user:
        flash('User with this email already exists.', 'danger')
        return redirect(url_for('main.admin_dashboard'))

    # Prepare user data with a 'created_at' field
    new_user = {
        'email': email,
        'password': generate_password_hash(password),  # Hash the password
        'role': role,
        'created_at': datetime.utcnow()  # Add the current UTC time
    }

    # Insert the new user into the MongoDB collection
    mongo.db.users.insert_one(new_user)

    flash(f'User {email} created successfully.', 'success')
    return redirect(url_for('main.admin_dashboard'))

# Notes:
# admin@admin.com - admin123
# remaining user - 123

# Admin can delete users
@main_bp.route('/delete_user/<user_id>')
@login_required
@role_required('admin')
def delete_user(user_id):
    users.delete_one({'_id': ObjectId(user_id)})
    flash('User deleted successfully.', 'success')
    return redirect(url_for('main.admin_dashboard'))

# Content-Mngt:
@main_bp.route('/dashboard/introduction')
@login_required
def introduction():
    role = session['role']
    # user_roles = current_user.roles  # Assuming 'current_user' is from Flask-Login
    return render_template('content/dashindex.html', role=role)

