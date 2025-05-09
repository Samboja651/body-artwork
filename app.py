"""art-experience"""

import os
from urllib.parse import urlparse
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, request, redirect, flash, url_for
from dotenv import load_dotenv
import psycopg2


load_dotenv(".env")

PAYMENT_LINK = os.getenv("PAYMENT_LINK")
BOOKING_LINK = os.getenv("BOOKING_LINK")
DATABASE = os.getenv("INTERNAL_DATABASE_URL")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET")
app.permanent_session_lifetime = datetime.timedelta(minutes=45)


# --------------------------
# configure & connect db
# --------------------------
def connect_db():
    """connect database"""
    result = urlparse(DATABASE)
    try:
        connection = psycopg2.connect(
            host=result.hostname,
            port=result.port,
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
        )
        print("db connected")
        return connection
    except (
        psycopg2.InterfaceError,
        psycopg2.ProgrammingError,
        psycopg2.DatabaseError,
    ) as e:
        return f"Connection Failed: {e}"


@app.get("/")
def home():
    """home page"""
    return render_template("home.html")


@app.get("/booking")
def booking():
    """book a session with art experience"""
    return render_template("booking.html", booking_link=BOOKING_LINK)


# @app.get('/about-us')
# def about():
#     """know more about art experience"""
#     return render_template("about.html")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    """Create user account"""
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("fname")
        last_name = request.form.get("lname")
        password = request.form.get("password")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save user details to the database
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO users (email, first_name, last_name, password)
                VALUES (%s, %s, %s, %s)
            """,
                (email, first_name, last_name, hashed_password),
            )
            conn.commit()
            conn.close()

            flash("Account created successfully!", "success")
            return redirect(url_for("sign_in"))
        except TypeError:
            conn.close()
            flash("Email already exists. Please use a different email.")
            return redirect(url_for("sign_up"))
        except psycopg2.IntegrityError:
            conn.close()
            flash("Email Already exist. Sign in.")
            return redirect(url_for("sign_up"))
        except Exception as e:
            conn.close()
            print(e)
            flash("Server under maintenance. Try later.")
            return redirect(url_for("sign_up"))

    return render_template("register.html")


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    """Sign in user"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Connect to the database
        conn = connect_db()
        cursor = conn.cursor()
        try:
            # Fetch the user by email
            cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            conn.close()

            if result:
                # Verify the password
                stored_password = result[0]
                if check_password_hash(stored_password, password):
                    flash("Signed in successfully!", "success")
                    return redirect(url_for("home"))
                flash("Invalid email or password.", "danger")

        except Exception as e:
            conn.close()
            print(e)
            flash("Server under maintenance. Try later.")
            return redirect(url_for("sign_in"))

    return render_template("login.html")
