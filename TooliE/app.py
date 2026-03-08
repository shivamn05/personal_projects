import os

import sqlite3
import datetime
from sqlite3 import IntegrityError
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_db

# Configure application 
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure session to use filesystem 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#  FOR HOMEPAGES 

# Manager homepage
@app.route("/managerhome")
@login_required
def managerhome():
    """Homepage for manager"""
    return render_template("managerhome.html")

# Employee homepage
@app.route("/employeehome")
@login_required
def employeehome():
    """Homepage for employee"""
    return render_template("employeehome.html")

# FOR ACCOUNT MANAGEMENT 

# Log In
@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("user_id"):
            return render_template("login.html", error="Please enter a User ID")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Please provide a password")

        # Query database for username
        db = get_db()
        rows = db.execute("SELECT * FROM users WHERE user_id = ?", (request.form.get("user_id"),))
        line = rows.fetchall()

        # Ensure username exists and password is correct
        if len(line) != 1 or not check_password_hash(
            line[0][3], request.form.get("password")
        ):
            return render_template("login.html", error="Invalid username or password")

        # Remember which user has logged in
        session["user_id"] = line[0][2]

        # Redirect user to home page
        if request.form.get("user_id")[0] == 'm':
            flash("Logged in successfully", "succcess")
            return redirect("/managerhome")
        elif request.form.get("user_id")[0] == 'e':
            flash("Logged in successfully", "success")
            return redirect("/employeehome")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
# Change password 
@app.route("/change", methods=["GET", "POST"])
def change():
    session.clear()
    if request.method == "POST":
        # Calling user_id and password
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        # Ensuring all fields are submitted
        if not user_id:
            return render_template("change.html", error="Please enter a User ID")
        if not password:
            return render_template("change.html", error="Please enter your new password")
        if not request.form.get("confirmation"):
            return render_template("change.html", error="Please confirm your new password")
        elif request.form.get("confirmation") != password:
            return render_template("change.html", error="Your passwords do not match")

        # Ensuring user exists to enable password to be updated
        db = get_db()
        existing_users = db.execute("SELECT user_id FROM users")
        user_found = False
        for user in existing_users:
            if (user_id == user["user_id"]):
                user_found = True
        if user_found == False:
            return render_template("change.html", error="User does not exist, please register instead")

        # Updating the password in the database
        db = get_db()
        db.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", (generate_password_hash(
            password, method='scrypt', salt_length=16), user_id))
        db.commit()

        return render_template("login.html")

    else:
        return render_template("change.html")

# Register new user 
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Enter Username
        username = request.form.get("username")
        if not username:
            return render_template("register.html", error="Please enter employee name")

        # Enter user ID
        user_id = request.form.get("user_id")
        if not user_id or len(user_id) != 5:
            return render_template("register.html", error="User ID should be 5 characters only")
        
        # Set default password
        db = get_db()
        try:
            default = generate_password_hash("Password")
            db.execute("INSERT INTO users (username, user_id, password_hash) VALUES(?, ?, ?)", (username, user_id, default))
            db.commit()
        except IntegrityError:
            return render_template("register.html", error="User ID already in use")

        # Go to Home Page
        flash("Successfully registered", "success")
        return redirect("/managerhome")

    else:
        return render_template("register.html")
    
# Log Out 
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# FOR EMPLOYEE MANAGEMENT 

# Show a list of all users 
@app.route("/employeelist", methods=["GET", "POST"])
@login_required
def employeelist():
    """Employee list for managers"""
    # Get all users from database
    db = get_db()
    users = db.execute("SELECT * FROM users ORDER BY username")
    return render_template("employeelist.html", users=users)

# Remove users 
@app.route("/remove", methods=["GET", "POST"])
@login_required
def remove():
    """Remove user from database"""
    user_id = request.form.get("user_id")
    db = get_db()
    db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    db.commit()
    db.execute("DELETE FROM bookings WHERE user_id = ?", (user_id,))
    db.commit()
    return redirect("/employeelist")

# FOR BOOKINGS 

# Booking a tool 
@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    """Booking a tool"""
    if request.method == "POST":
        # Pulling values from form 
        tool = request.form.get("tool")
        raw_date = request.form.get("date")
        date_temp = datetime.datetime.strptime(raw_date, "%Y-%m-%d")
        date_format = date_temp.strftime("%d-%m-%Y")
        timeslot = request.form.get("timeslot")

        # Ensuring values are submitted
        if not tool:
            flash("Please select tool")
            return redirect("/book")
        if not raw_date:
            flash("Please select date")
            return redirect("/book")
        if not timeslot:
            flash("Please select a timeslot")
            return redirect("/book")
        
        # Ensuring values are valid
        valid_letters = ["A", "B", "C", "D", "E"]
        valid_timeslot = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

        if tool not in valid_letters:
            flash("Select tool from list only")
            return redirect("/book")
        if timeslot not in valid_timeslot:
            flash("Select available timeslots only")
            return redirect("/book")

        # Inserting booking into database
        db = get_db()
        existing = db.execute("SELECT * FROM bookings WHERE tool_name = ? AND date = ? AND timeslot = ?", (tool, date_format, timeslot,)).fetchall()
        if existing:
            flash("Timeslot not available")
            return redirect("/book")
        else: 
            db.execute("INSERT INTO bookings (user_id, tool_name, date, timeslot) VALUES (?, ?, ?, ?)", (session["user_id"], tool, date_format, timeslot))
            db.commit()
            return redirect("/bookings")
    else:
        # For dropdown in tool booking
        letters = ["A", "B", "C", "D", "E"]
        # For date for 2 weeks 
        # Source: ChatGPT
        today = datetime.date.today()
        two_weeks_later = today + datetime.timedelta(days=14)
        dates = []
        for i in range((two_weeks_later-today).days + 1):
            d = today + datetime.timedelta(days=i)
            dates.append({
                "value": d.isoformat(),
                "label": d.strftime("%d-%m-%Y (%A)")
            })
        return render_template("book.html", letters=letters, dates=dates, today=today.isoformat(), max_date=two_weeks_later.isoformat()) 

# Show a list of personal bookings 
@app.route("/bookings", methods=["GET", "POST"])
@login_required
def userbookings():
    """Shows bookings"""
    db = get_db()
    bookings = db.execute("SELECT * FROM bookings WHERE user_id = ? ORDER BY date, timeslot", (session["user_id"],))
    return render_template("bookings.html", bookings=bookings)

# Show a list of everyone's bookings for managers 
@app.route("/allbookings", methods=["GET", "POST"])
@login_required
def allbookings():
    """Shows manager all the bookings"""
    db = get_db()
    bookings = db.execute("SELECT bookings.*, users.username FROM bookings JOIN users ON bookings.user_id = users.user_id ORDER BY date, timeslot")
    return render_template("allbookings.html", bookings=bookings)

# Mark a booking as completed
@app.route("/completedbooking", methods=["GET", "POST"])
@login_required
def completedbooking():
    """Mark a booking as completed"""
    # Get from form 
    user_id = request.form.get("user_id")
    tool_name = request.form.get("tool_name")
    date_format = request.form.get("date")
    timeslot = request.form.get("timeslot")

    db = get_db()
    # Insert into history as Completed
    db.execute("INSERT INTO history (user_id, tool_name, date, timeslot, status) VALUES (?, ?, ?, ?, ?)", (user_id, tool_name, date_format, timeslot, "Completed",))
    db.commit()
    # Remove from current bookings
    db.execute("DELETE FROM bookings WHERE user_id = ? AND tool_name = ? AND date = ? AND timeslot = ?", (user_id, tool_name, date_format, timeslot,))
    db.commit()

    return redirect("/bookings")

# Remove a booking 
@app.route("/removebooking", methods=["GET", "POST"])
@login_required
def removebooking():
    """Remove a booking"""
    # Get from form 
    user_id = request.form.get("user_id")
    tool_name = request.form.get("tool_name")
    date_format = request.form.get("date")
    timeslot = request.form.get("timeslot")

    db = get_db()
    # Insert into history as Deleted
    db.execute("INSERT INTO history (user_id, tool_name, date, timeslot, status) VALUES (?, ?, ?, ?, ?)",(user_id, tool_name, date_format, timeslot, "Deleted",))
    db.commit()
    # Remove from current bookings
    db.execute("DELETE FROM bookings WHERE user_id = ? AND tool_name = ? AND date = ? AND timeslot = ?", (user_id, tool_name, date_format, timeslot,))
    db.commit()

    return redirect("/bookings")

# Show a list of personal booking history and status 
@app.route("/bookinghistory", methods=["GET", "POST"])
@login_required
def bookinghistory():
    """Show personal history"""
    db = get_db()
    history = db.execute("SELECT * FROM history WHERE user_id = ? ORDER BY date, timeslot", (session["user_id"],))
    return render_template("bookinghistory.html", history=history)

# Show a list of everyone's booking history and status
@app.route("/bookinghistorymgr", methods=["GET", "POST"])
@login_required
def allbookinghistory():
    """Show personal history"""
    db = get_db()
    history = db.execute("SELECT history.*, users.username FROM history JOIN users ON history.user_id = users.user_id ORDER BY date, timeslot")
    return render_template("bookinghistorymgr.html", history=history)