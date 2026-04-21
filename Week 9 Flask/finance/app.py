import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime
from datetime import date
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "roundx"])
@login_required
def index():
    """Show portfolio of stocks"""
    price = {}
    current = {}
    Value = {}
    data = db.execute("SELECT name, symbol, quantity, amount FROM stocks WHERE userid = :user", user=session["user_id"])
    Balance = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])
    Total = Balance[0]["cash"]
    for i in data:
        Value[i["symbol"]] = lookup(i["symbol"])["price"] * int(i["quantity"])
        price[i["symbol"]] = lookup(i["symbol"])["price"]
        Total = Total + Value[i["symbol"]]
    Balance = int(float(Balance[0]["cash"]))
    return render_template("/index.html", price=price, current=current, Value=Value, Balance=Balance, data=data, Total=Total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        Cash = db.execute("SELECT cash FROM users WHERE id=:userid", userid=session["user_id"])
        Symbol = request.form.get("symbol")
        Share = request.form.get("shares")

        if Share.isdigit() != True:
            return apology("Invalid Quantity")

        elif Symbol == None:
            return apology("Symbol required")

        elif Share == None:
            return apology("Invalid quantity")

        elif lookup(Symbol) == None:
            return apology("Invalid symbol")

        elif Cash[0]["cash"] < lookup(Symbol)["price"] * int(Share):
            return apology("Insufficient funds")

        else:
            today = date.today()
            day = today.strftime("%d/%m/%Y")
            now = datetime.now()
            Time = now.strftime("%H:%M:%S")
            amount = lookup(Symbol)["price"] * int(request.form.get("shares"))
            update = db.execute("UPDATE users SET cash=:amt WHERE id=:userid ",
                                amt=Cash[0]["cash"] - amount, userid=session["user_id"])
            check = db.execute("SELECT symbol FROM stocks WHERE symbol=:symbol AND userid=:userid",
                               symbol=Symbol, userid=session["user_id"])
            if len(check) == 0:
                update_holdings = db.execute("INSERT INTO stocks (userid,symbol,name,quantity, amount ,time, day) VALUES (:userid,:symbol,:name,:quantity, :amount, :time, :day)",
                                             userid=session["user_id"], symbol=Symbol, name=lookup(Symbol)["name"], quantity=Share, amount=amount, time=Time, day=day)
            else:
                quant = db.execute("SELECT quantity FROM stocks WHERE userid=:userid AND symbol=:symbol ",
                                   userid=session["user_id"], symbol=Symbol)
                update_holdings = db.execute("UPDATE stocks SET quantity=:q WHERE symbol=:symbol AND userid=:userid",
                                             q=int(quant[0]["quantity"]) + int(Share), symbol=Symbol, userid=session["user_id"])
            flash('Bought!')
            return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    input = db.execute("SELECT name, symbol, amount, time, day FROM stocks WHERE userid = :userid", userid=session["user_id"])
    if len(input) == 0:
        return apology("No purchase history")
    else:
        return render_template("/history.html", input=input)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        Symbol = request.form.get("symbol")
        if lookup(Symbol) == None:
            return apology("Invalid Symbol")
        else:
            foo = lookup(Symbol)
            bar = db.execute("SELECT cash FROM users WHERE id =:id", id=session["user_id"])
            affordable = bar[0]["cash"] / foo["price"]
            bar = int(float(bar[0]["cash"]))
            return render_template("quoted.html", foo=foo, affordable=affordable, bar=bar)


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        check = db.execute("SELECT * FROM users WHERE username=:username", username=username)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if len(username) == 0 or len(password) == 0 or len(confirmation) == 0:
            return apology("You must fill all fields")

        elif len(check) > 0:
            return apology("Username not available")

        elif password != confirmation:
            return apology("Passwords do not match")

        else:
            rows = db.execute("INSERT INTO users (username,hash) VALUES (:username,:password)", username=username,
                              password=generate_password_hash(confirmation, method='pbkdf2:sha256', salt_length=8))
            check = db.execute("SELECT * FROM users WHERE username=:username", username=username)
            session["user_id"] = check[0]["id"]
            flash('Registered!')
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        options = db.execute("SELECT symbol, quantity FROM stocks WHERE userid= :userid",
                             userid=session["user_id"])
        return render_template("sell.html", options=options)
    else:
        Cash = db.execute("SELECT cash FROM users WHERE id = (?)", (session["user_id"]))
        Symbol = request.form.get("symbol")
        Share = request.form.get("shares")
        currentshare = db.execute("SELECT quantity FROM stocks WHERE userid = :userid AND symbol = :Symbol",
                                  userid=session["user_id"], Symbol=Symbol)

        if Share.isdigit() == True:
            Share = int(Share)
        else:
            return apology("Invalid Quantity")

        if Symbol == None:
            return apology("Input Symbol")

        elif lookup(Symbol) == None:
            return apology("Invalid Symbol")

        elif int(Share) <= 0:
            return apology("Input Quantity")

        else:
            for i in currentshare:
                baz = int(i["quantity"])
                if Share > baz:
                    return apology("Invalid Share quantity")
                else:
                    amount = lookup(Symbol)["price"] * Share
                    Total = Cash[0]["cash"] + amount
                    userid = session["user_id"]
                    update = db.execute("UPDATE stocks SET quantity = :bar WHERE userid = :userid",
                                        bar=baz - Share, userid=session["user_id"])
                    profit = db.execute("UPDATE users SET cash= :Total WHERE id = :userid",
                                        Total=Total, userid=userid)
                    flash("Sold!")
                    return redirect("/")

        return apology("how did I get here?")


@app.route("/addcash", methods=["GET", "POST"])
@login_required
def AddCash():
    """Add cash to account"""

    if request.method == "GET":
        return render_template("addcash.html")
    else:
        Newamount = request.form.get("addcash")
        Currentcash = db.execute("SELECT cash FROM users WHERE id = :userid", userid=session["user_id"])
        if Newamount.isdigit() == True:
            Newamount = int(Newamount)
        else:
            return apology("Invalid Quantity")

        Total = Newamount + Currentcash[0]["cash"]
        Update = db.execute("UPDATE users SET cash = :Total", Total=Total)

        return redirect("/")