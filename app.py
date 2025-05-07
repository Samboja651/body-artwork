"""art-experience"""
import os
import sqlite3
import datetime
import bcrypt
from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
from setup_db import setup_db

load_dotenv('.env')

PAYMENT_LINK = os.getenv('PAYMENT_LINK')
BOOKING_LINK = os.getenv('BOOKING_LINK')

app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
app.permanent_session_lifetime = datetime.timedelta(minutes=45)

# setup database
setup_db()

@app.get("/")
def home():
    """home page"""
    return render_template("home.html")

@app.get("/booking")
def booking():
    """book a session with art experience"""
    return render_template("booking.html", booking_link=BOOKING_LINK)

@app.get('/about-us')
def about():
    """know more about art experience"""
    return render_template("about.html")

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    """Create user account"""
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('fname')
        last_name = request.form.get('lname')
        password = request.form.get('password')

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Save user details to the database
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (email, first_name, last_name, password)
                VALUES (?, ?, ?, ?)
            ''', (email, first_name, last_name, hashed_password))
            conn.commit()
            conn.close()

            flash("Account created successfully!", "success")
            return redirect(url_for('sign_in'))
        except sqlite3.IntegrityError:
            flash("Email already exists. Please use a different email.")
            return redirect(url_for('sign_up'))
        except sqlite3.OperationalError as e:
            flash("Server Downtime. Try again later.")
            print(e)
            return redirect(url_for('sign_up'))

    return render_template('register.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    """Sign in user"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            # Connect to the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Fetch the user by email
            cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # Verify the password
                stored_password = result[0]
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    flash("Signed in successfully!", "success")
                    return redirect(url_for('home'))
                flash("Invalid email or password.", "danger")

        except sqlite3.OperationalError as e:
            flash("Server Downtime. Try again later.")
            print(e)
            return redirect(url_for('sign_in'))

    return render_template("login.html")
