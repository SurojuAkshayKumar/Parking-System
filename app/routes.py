from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.models import User, ParkingSpot, Booking
from app.forms import LoginForm, RegistrationForm

# Route for the home page
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# User logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route for booking parking spots
@app.route('/book/<int:spot_id>', methods=['GET', 'POST'])
@login_required
def book(spot_id):
    # Implement the booking logic here
    flash(f'Parking spot {spot_id} booked successfully!', 'success')
    return redirect(url_for('index'))

# Admin dashboard route
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Verify if the user is an admin
    if not current_user.is_admin:  # Assumes 'is_admin' attribute in User model
        flash('Access denied: You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    # Retrieve data for admin dashboard
    users = User.query.all()
    bookings = Booking.query.all()
    spots = ParkingSpot.query.all()
    return render_template('admin_dashboard.html', users=users, bookings=bookings, spots=spots)

# Additional routes for admin functionalities can be added here...

# Add more routes as needed...

