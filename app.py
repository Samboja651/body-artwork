"""art-experience"""
from flask import Flask, render_template


app = Flask(__name__)


@app.get("/")
def home():
    """home page"""
    return render_template("home.html")

@app.get("/booking")
def booking():
    """book a session with art experience"""
    return render_template("booking.html")

@app.get('/about')
def about():
    """know more about art experience"""
    return render_template("about.html")
