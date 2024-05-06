import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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
    # Get user's cash balance
    user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]

    # Get user's stocks and their current prices
    stocks = db.execute("""
        SELECT symbol, SUM(shares) AS total_shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
    """, session["user_id"])

    # Prepare data to render
    portfolio = []
    total_value = user_cash

    for stock in stocks:
        symbol = stock["symbol"]
        total_shares = stock["total_shares"]
        stock_info = lookup(symbol)

        if stock_info:
            price_per_share = stock_info["price"]
            total_value += price_per_share * total_shares
            portfolio.append({
                "symbol": symbol,
                "shares": total_shares,
                "price_per_share": price_per_share,
                "total_value": price_per_share * total_shares
            })

    return render_template("index.html", portfolio=portfolio, cash=user_cash, total_value=total_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        # Ensure symbol was submitted
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure shares was submitted
        shares = request.form.get("shares")
        if not shares:
            return apology("must provide shares", 400)

        # Ensure shares is a positive integer
        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("shares must be a positive integer", 400)

        # Get current price of the stock
        stock_info = lookup(symbol)
        if not stock_info:
            return apology("invalid symbol", 400)

        price_per_share = stock_info["price"]

        # Calculate total cost
        total_cost = price_per_share * shares

        # Check if the user can afford the purchase
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        if total_cost > user_cash:
            return apology("insufficient funds", 403)

        # Perform the purchase
        db.execute("""
            INSERT INTO transactions (user_id, symbol, shares, price_per_share, total_cost, transaction_type, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, session["user_id"], symbol, shares, price_per_share, total_cost, "buy", price_per_share)  # Insert price

        # Update user's cash balance
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", total_cost, session["user_id"])

        # Redirect to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    # Retrieve user's transaction history
    transactions = db.execute("""
        SELECT symbol, shares, price, transacted_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY transacted_at DESC
    """, session["user_id"])

    return render_template("history.html", transactions=transactions)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide stock symbol", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("invalid stock symbol", 400)

        print("Quote data:", quote)  # Add this line to check quote data

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        password = request.form.get("password")
        if not password:
            return apology("must provide password", 400)

        # Ensure password confirmation matches
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return apology("passwords do not match", 400)

        # Check if username already exists
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if existing_user:
            return apology("username already exists", 400)

        # Hash password and insert new user into database
        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hashed_password)

        # Redirect user to login page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        # Ensure symbol and shares were submitted
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        if not shares:
            return apology("must provide shares", 400)

        # Ensure shares is a positive integer
        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("shares must be a positive integer", 400)

        # Get user's available shares of the given symbol
        user_shares = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        if not user_shares or user_shares[0]["shares"] < shares:
            return apology("not enough shares to sell", 400)

        # Get current price of the stock
        stock_info = lookup(symbol)
        if not stock_info:
            return apology("invalid symbol", 400)

        price_per_share = stock_info["price"]

        # Calculate total sale value
        sale_value = price_per_share * shares

        # Update user's cash balance
        user_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   user_cash + sale_value, session["user_id"])

        # Update user's portfolio
        remaining_shares = user_shares[0]["shares"] - shares
        if remaining_shares == 0:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?",
                       session["user_id"], symbol)
        else:
            db.execute("UPDATE portfolio SET shares = ? WHERE user_id = ? AND symbol = ?",
                       remaining_shares, session["user_id"], symbol)

        # Add transaction to history
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price_per_share, total_cost, transaction_type) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbol, -shares, price_per_share, sale_value, "sell")

        flash("Sold successfully!")
        return redirect("/")

    else:
        # Get symbols of stocks user owns
        stocks = db.execute("SELECT symbol FROM portfolio WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0",
                            session["user_id"])

        return render_template("sell.html", stocks=stocks)
