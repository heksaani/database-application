"""This module contains the routes for the application."""
from flask import render_template, request, redirect, session
import users
from app import app

@app.route("/")
def index():
    """Index handler"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login handler"""
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    if users.login(username, password):
        return redirect("/")

    return render_template("error.html", message="Wrong credentials")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration handler"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords do not match")

        role = int(request.form["type"])
        status = "user"
        leader = False

        if role == 1:
            status = "leader"
            leader = True

        if users.register(username, password1, leader):
            return render_template("first_page.html", username=username, role=status)

        return render_template("error.html", message="Registaation failed, username already exists")


    return render_template("error.html", message="Unknown error")


@app.route("/logout")
def logout():
    """Logout handler"""
    users.logout()
    return redirect("/")


@app.route("/error")
def error():
    """Error handler"""
    return render_template("error.html")