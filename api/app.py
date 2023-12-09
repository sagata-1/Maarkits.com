import os

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import pytz
from helpers import apology, login_required, lookup, usd, answer, total_computation

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Configure database connection
con = psycopg2.connect(dbname="postgres", user="postgres", password="Saucepan03@!", host="db.krvuffjhmqiyerbpgqtv.supabase.co")
db = con.cursor(cursor_factory=RealDictCursor)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    db.execute(
        "SELECT * FROM portfolios WHERE user_id = (%s)", (session["user_id"],)
    )
    portfolio = db.fetchall()
    for stock in portfolio:
        db.execute(
            "UPDATE portfolios set price = (%s) WHERE user_id = (%s) AND stock_symbol = (%s)",
            (lookup(stock["stock_symbol"])["price"],
            session["user_id"],
            stock["stock_symbol"])
        )
        con.commit()
    db.execute("SELECT * FROM users WHERE id = (%s)", (session["user_id"],))
    cash = db.fetchall()
    cash = float(cash[0]["cash"])
    db.execute(
        "SELECT * FROM portfolios WHERE user_id = (%s) ORDER BY stock_symbol",
        (session["user_id"],)
    )
    portfolio = db.fetchall()
    total = cash
    for stock in portfolio:
        total += stock["price"] * stock["num_shares"]
    db.execute("SELECT username FROM users WHERE id = (%s)", (session["user_id"],))
    username = db.fetchall()
    username = username[0]["username"]
    symbols = ["TSLA", "AAPL", "GOOG"]
    assets = []
    for elem in symbols:
        assets.append(lookup(elem))
    return render_template("index.html", portfolio=portfolio, cash=usd(cash), total=usd(total), username=username, assets=assets)

@app.route("/learn", methods=["GET", "POST"])
@login_required
def learn():
    if request.method == "POST":
        question = request.form.get("symbol")
        _answer = answer(question)
        return render_template("answer.html", _answer=_answer)
    db.execute("SELECT username FROM users WHERE id = (%s)", (session["user_id"],))
    username = db.fetchall()
    username = username[0]["username"]
    symbols = ["TSLA", "AAPL", "GOOG"]
    assets = []
    for elem in symbols:
        assets.append(lookup(elem))
    return render_template("learn.html", username=username, assets=assets)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    symbol = request.form.get("symbol").upper()
    num_shares = request.form.get("shares")
    stock = lookup(symbol)
    # Error checking (i.e. missing symbol, too many shares bought etc)
    if not stock:
        return apology("Invalid Symbol", 400)
    if not num_shares.isdigit():
        return apology("Invalid Shares", 400)
    num_shares = int(num_shares)
    if num_shares < 0:
        return apology("Invalid Shares", 400)
    price = stock["price"]
    db.execute("SELECT * FROM users WHERE id = (%s)", (session["user_id"],))
    user = db.fetchall()
    if (num_shares * price) > user[0]["cash"]:
        return apology("Cannot Afford", 400)
    db.execute(
        "SELECT * FROM portfolios WHERE user_id = (%s) AND stock_symbol = (%s)",
        (session["user_id"],
        symbol)
    )
    portfolio = db.fetchall()
    # Start a stock for a new user if it doesn't exist
    time = datetime.datetime.now(pytz.timezone("UTC")).strftime("%Y-%m-%d %H:%M:%S")
    if (len(portfolio)) == 0:
        db.execute(
            "INSERT INTO portfolios(user_id, stock_name, stock_symbol, price, num_shares, time_bought) VALUES(%s, %s, %s, %s, %s, %s)",
            (session["user_id"],
            stock["name"],
            stock["symbol"],
            price,
            num_shares,
            time)
        )
        con.commit()
        db.execute(
            "INSERT INTO history(user_id, stock_symbol, price, num_shares, time_of_transaction) VALUES(%s, %s, %s, %s, %s)",
            (session["user_id"],
            stock["symbol"],
            price,
            num_shares,
            time)
        )
        con.commit()
        db.execute(
            "UPDATE users SET cash = cash - (%s) WHERE id = (%s)",
            (num_shares * price,
            session["user_id"])
        )
        con.commit()
    # Update current portfolio
    else:
        db.execute(
            "UPDATE portfolios SET price = (%s), num_shares = num_shares + (%s) WHERE user_id = (%s) and stock_symbol = (%s)",
            (price,
            num_shares,
            session["user_id"],
            stock["symbol"])
        )
        con.commit()
        db.execute(
            "INSERT INTO history(user_id, stock_symbol, price, num_shares, time_of_transaction) VALUES(%s, %s, %s, %s, %s)",
            (session["user_id"],
            stock["symbol"],
            price,
            num_shares,
            time)
        )
        con.commit()
        db.execute(
            "UPDATE users SET cash = cash - (%s) WHERE id = (%s)",
            (num_shares * price,
            session["user_id"])
        )
        con.commit()
    flash("Bought!")
    return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    db.execute(
        "SELECT * FROM history WHERE user_id = (%s) ORDER BY time_of_transaction",
        (session["user_id"],)
    )
    user_history = db.fetchall()
    db.execute("SELECT username FROM users LIMIT 10")
    usernames = db.fetchall()
    for username in usernames:
        username["total"] = total_computation(username["username"])[0]
    usernames = sorted(usernames, key=lambda a: a["total"], reverse=True)
    return render_template("history.html", history=user_history, usernames=usernames, size=len(usernames))

@app.route("/beginner")
@login_required
def beginner():
    return render_template("beginner.html")


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
        db.execute("SELECT * FROM users WHERE username = (%s)", (request.form.get("username"),))
        rows = db.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    symbol = request.form.get("symbol")
    stock = lookup(symbol)
    if not stock:
        return apology("Invalid Symbol", 400)
    return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            return ("Please provide a username", 400)
        db.execute("SELECT username FROM users WHERE username = (%s)", (username,))
        database_username = db.fetchall()
        if (
            len(database_username)
            > 0
        ):
            return apology("username already exists", 400)
        password = request.form.get("password")
        password_check = request.form.get("confirmation")
        if password != password_check or not password:
            return apology("passwords do not match / did not enter a password", 400)
        # Register user
        db.execute("INSERT INTO users (username, hash) VALUES(%s, %s)", (username,generate_password_hash(password)))
        con.commit()
        db.execute("SELECT id FROM users WHERE username = (%s)", (username,))
        user = db.fetchall()
        # Log user in  after registration
        session["user_id"] = user[0]["id"]
        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    db.execute(
        "SELECT stock_symbol FROM portfolios WHERE user_id = (%s)", (session["user_id"],)
    )
    valid_symbols = db.fetchall()
    if request.method == "GET":
        return render_template("sell.html", symbols=valid_symbols)
    symbol = request.form.get("symbol").upper()
    num_shares = request.form.get("shares")
    db.execute(
        "SELECT * FROM portfolios WHERE stock_symbol = (%s) AND user_id = (%s)",
        (symbol,
        session["user_id"])
    )
    stock = db.fetchall()
    # Error checking (i.e. missing symbol, too many shares sold etc)
    if len(stock) != 1:
        return apology("Invalid Symbol", 400)
    if not num_shares.isdigit():
        return apology("Invalid Shares", 400)
    num_shares = (int(num_shares)) * -1
    if num_shares > 0:
        return apology("Invalid Shares", 400)
    if stock[0]["num_shares"] + num_shares < 0:
        return apology("Too many shares", 400)
    # Keep track of sells
    time = datetime.datetime.now(pytz.timezone("UTC")).strftime("%Y-%m-%d %H:%M:%S")
    # Update current portfolio
    price = lookup(symbol)["price"]
    if stock[0]["num_shares"] + num_shares == 0:
        db.execute(
            "DELETE FROM portfolios WHERE user_id = (%s) AND stock_symbol = (%s)",
            (session["user_id"],
            symbol)
        )
        con.commit()
        db.execute(
            "INSERT INTO history(user_id, stock_symbol, price, num_shares, time_of_transaction) VALUES(%s, %s, %s, %s, %s)",
            (session["user_id"],
            symbol,
            price,
            num_shares,
            time)
        )
        con.commit()
        db.execute(
            "UPDATE users SET cash = cash - (%s) WHERE id = (%s)",
            (num_shares * price,
            session["user_id"])
        )
        con.commit()
    else:
        db.execute(
            "UPDATE portfolios SET price = (%s), num_shares = num_shares + (%s) WHERE user_id = (%s) AND stock_symbol = (%s)",
            (price,
            num_shares,
            session["user_id"],
            symbol)
        )
        con.commit()
        db.execute(
            "INSERT INTO history(user_id, stock_symbol, price, num_shares, time_of_transaction) VALUES(%s, %s, %s, %s, %s)",
            (session["user_id"],
            symbol,
            price,
            num_shares,
            time)
        )
        con.commit()
        db.execute(
            "UPDATE users SET cash = cash - (%s) WHERE id = (%s)",
            (num_shares * price,
            session["user_id"])
        )
        con.commit()
    flash("Sold!")
    return redirect("/")


@app.route("/password-change", methods=["GET", "POST"])
@login_required
def password_change():
    if request.method == "GET":
        return render_template("password_change.html")
    db.execute("SELECT * FROM users WHERE id = (%s)", (session["user_id"],))
    prev_password = db.fetchall()
    prev_password = prev_password[0]["hash"]
    if not check_password_hash(prev_password, request.form.get("curr_password")):
        return apology("Invalid Current Password", 400)
    new_password = request.form.get("new_password")
    if new_password != request.form.get("confirmation") or not new_password:
        return apology(
            "Please make sure you have confirmed your password / chosen a new password",
            400,
        )
    db.execute(
        "UPDATE users SET hash = (%s) WHERE id = (%s)",
        (generate_password_hash(new_password),
        session["user_id"])
    )
    con.commit()
    flash("Password Changed!")
    return redirect("/")

@app.route("/landing", methods=["GET"])
def layout():
    return render_template("trial_1.html")

if __name__ == "__main__":
    app.run()