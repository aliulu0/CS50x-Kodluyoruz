import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    if request.method == "POST":
        db.execute("""
        UPDATE users
        SET cash = cash + :amount
        WHERE id = :user_id""", amount = request.form.get("cash"), user_id=session["user_id"])

        flash("Added Cash!")
        return redirect("/")

    else:
        return render_template("add_cash.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":

        older = request.form.get("old_pass")
        new = request.form.get("new_pass")
        confirmation = request.form.get("confirmation")
        hash = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])

        if not check_password_hash(hash[0]["hash"],older):
            return apology("Password is wrong")

        elif new != confirmation:
            return apology("Passwords didn't match")

        new_hash = generate_password_hash(new)
        db.execute("UPDATE users SET hash=:new_hash WHERE id=:id", new_hash = new_hash, id=session["user_id"])

        flash("Changed Password!")
        return redirect("/")

    else:
        return render_template("change_password.html")



@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    rows = db.execute("""
        SELECT symbol, SUM(shares) as totalShares
        FROM transactions WHERE user_id = :user_id
        GROUP BY symbol
        HAVING totalShares > 0;
    """, user_id = session["user_id"])

    companys = []
    sum_price = 0
    for row in rows:
        stock = lookup(row["symbol"])
        companys.append({
            "symbol": stock["symbol"],
            "name": stock["name"],
            "shares": row["totalShares"],
            "price": usd(stock["price"]),
            "total": usd(stock["price"] * row["totalShares"])
        })
        sum_price += stock["price"] * row["totalShares"]
    rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id = session["user_id"])
    cash = rows[0]["cash"]
    sum_price += cash

    return render_template("index.html", companys=companys, cash = usd(cash), sum_price = usd(sum_price))




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        symbol= request.form.get("symbol").upper()
        count = int(request.form.get("shares"))

        if not symbol:
            return apology("must provide symbol", 400)
        if not count:
            return apology("must provide count", 400)

        if count<=0:
            return apology("Shares must be a positive number", 400)
        stock = lookup(symbol)
        if not stock:
            return apology("Symbol is not found", 400)

        price = stock['price']

        rows = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        cash = rows[0]["cash"]

        update_cash = cash - (count * price)

        if update_cash < 0:
            return apology("Your cash is not enough to buy shares", 400)
        db.execute("UPDATE users SET cash= :update_cash WHERE id= :id ", update_cash=update_cash, id = session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
        user_id = session["user_id"], symbol = symbol, shares = count, price = price
        )
        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")



@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    return jsonify("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute("""
        SELECT symbol, shares, price, transacted
        FROM transactions
        WHERE user_id = :user_id
    """,user_id = session["user_id"])

    for i in range(len(transactions)):
        transactions[i]["price"] = usd(transactions[i]["price"])

    return render_template("history.html",transactions = transactions)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

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

    if request.method == "POST":

        symbol = request.form.get("symbol").upper()

        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)
        if not stock:
            return apology("Symbol is not found", 400)

        else:
            return render_template("quoted.html", stock = stock)

    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":

        if not username:
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not confirmation:
            return apology("must provide password", 403)

        user = db.execute("SELECT username from users WHERE username = :username", username = username)
        if user:
            return apology("username is not avaliable")

        elif confirmation != password:
            return apology("Passwords didn't match", 400)

        #Query
        hash = generate_password_hash(password)

        rows = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username = username, hash = hash)

        if rows:
            return apology("username is not avaliable")

        session["user_id"] = rows["id"]

        return redirect("/")


    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":

        symbol= request.form.get("symbol").upper()
        count = int(request.form.get("shares"))

        if not symbol:
            return apology("must provide symbol", 403)
        if not count:
            return apology("must provide count", 403)

        if count<=0:
            return apology("Shares must be a positive number", 403)
        stock = lookup(symbol)
        if not stock:
            return apology("Symbol is not found", 400)

        rows = db.execute("""
            SELECT symbol, SUM(shares) as totalShares
            FROM transactions WHERE user_id = :user_id
            GROUP BY symbol
            HAVING totalShares > 0;
        """, user_id = session["user_id"])
        for row in rows:
            if row["symbol"] == symbol:
                if count > row["totalShares"]:
                    return apology("too many shares")

        rows = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        cash = rows[0]["cash"]
        price = stock['price']

        update_cash = cash + (count * price)
        db.execute("UPDATE users SET cash= :update_cash WHERE id= :id ", update_cash=update_cash, id = session["user_id"])


        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES(:user_id, :symbol, :shares, :price)",
        user_id = session["user_id"], symbol = symbol, shares = -1 * count, price = price)
        flash("Sold!")
        return redirect("/")
    else:
        rows = db.execute("""
            SELECT symbol
            FROM transactions
            WHERE user_id = :user_id
            GROUP BY symbol
            HAVING SUM(shares) > 0;
        """, user_id = session["user_id"])
        return render_template("sell.html", symbols = [ row['symbol'] for row in rows ])

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
