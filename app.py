import os
import datetime 

from cs50 import SQL
from flask import Flask,flash,redirect,render_template, request,session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

app = Flask(__name__)

app.config["SESSION PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)

db = SQL("sqlite:///data.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"]= "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method == "POST":
        if not request.form.get("username"):
            return render_template("apology.html", placeholder="Username field cannot be blank")
        if not request.form.get("password"):
            return render_template("apology.html", placeholder="Password field cannot be blank")
        user=db.execute("SELECT id FROM users WHERE username=?",request.form.get("username"))
        passw=db.execute("SELECT hash FROM users WHERE username=?",request.form.get("username"))
        if (user==[]):
            return render_template("apology.html", placeholder = "User doesnt exist in our records")
        if (check_password_hash(passw[0]["hash"], request.form.get("password"))== False) :
            return render_template("apology.html", placeholder="Password does not match")
        session["user_id"]=user[0]["id"]
        print(session["user_id"])
        return redirect("/")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    if request.method=="POST":
        if not request.form.get("username"):
            return render_template("apology.html", placeholder="Username field cannot be blank")
        if not request.form.get("password"):
             return render_template("apology.html", placeholder="Password field cannot be blank")
        if not request.form.get("pass"):
             return render_template("apology.html", placeholder="Password verification field cannot be blank")
        usernames=db.execute("SELECT username FROM users")
        for i in usernames:
            if (usernames[0]["username"]==request.form.get("username")):
                return render_template("apology.html", placeholder="Username already exists")
        if(request.form.get("password") != request.form.get("pass")):
            return render_template("apology.html", placehodler="password field must be the same")
        password1 = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username,hash) VALUES (?,?)", request.form.get("username"), password1)
        return redirect("/")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/ourservice")
def service() :
    return render_template("ourservice.html")



       
    
@app.route("/")
def index():
    return render_template("index.html")



        
        




