import os

from cs50 import SQL
from flask import Flask, redirect, render_template, request
from flask_session import Session


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///Worldcities.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/City", methods=["GET", "POST"])
def city():
    if request.method == "GET":
        render_template("/index.html")
    else:
        City = request.form.get("CurrentCity")
        if len(City) == 0:
            error = "Please enter a City"
            check = len(error)
            return render_template("/output.html", error=error, check=check)

        elif all(j.isalpha() or j.isspace() for j in City):
            check = 0

        else:
            error = "Only letters are in input"
            check = len(error)
            return render_template("/output.html", error=error, check=check)

        City = City.title()
        data = db.execute("SELECT * FROM mytable WHERE city = :City", City=City)
        if len(data) != 0:
            Latitude = data[0]["lat"]
            Longitude = data[0]["lng"]
            City = data[0]["city"]
            Country = data[0]["country"]
            Population = data[0]["population"]
            check = 0
            return render_template("/output.html", Longitude=Longitude, Latitude=Latitude, City=City, Country=Country, Population=Population, check=check)
        else:
            error = "Invalid City"
            check = len(error)
            return render_template("/output.html", error=error,check=check)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("/index.html")
    else:
        return redirect("/")