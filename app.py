"""art-experience"""
import os
from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv('.env')

PAYMENT_LINK = os.getenv('PAYMENT_LINK')
BOOKING_LINK = os.getenv('BOOKING_LINK')

app = Flask(__name__)


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
