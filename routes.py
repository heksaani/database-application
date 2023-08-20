"""This module contains the routes for the application."""
from datetime import datetime
import secrets
from flask import render_template, request, redirect, session, abort
import users
import tasks
import groups
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
            # Generate a new CSRF token for the session
            session["csrf_token"] = secrets.token_urlsafe()
            return redirect("/")
        else:
            return render_template("error.html", message="Invalid username or password")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration handler"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        session["csrf_token"] = secrets.token_urlsafe()
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

        return render_template("error.html", message="Registration failed, username already exists")


    return render_template("error.html", message="Unknown error")

@app.route("/logout")
def logout():
    """Logout handler"""
    users.logout()
    return redirect("/")

#in progress
@app.route("/createTask", methods=["GET", "POST"])
def create_task():
    """Task creation handler"""
    print("Entered create_task route")  # Add this line
    if request.method == "GET":
        return render_template("createTask.html")
    if request.method == "POST":
        print(request.form)  # Print the entire form data
        try:
            print(f"CSRF token: {session['csrf_token']}")  # Print the CSRF token
            print(f"Form CSRF token: {request.form['csrf_token']}")  # Print the CSRF token
            if session["csrf_token"] != request.form["csrf_token"]:
                abort(403)
        except KeyError as ex:
            print(f"Error accessing CSRF token: {ex}")
            return render_template("error.html", message="Error accessing CSRF token")
        name = request.form["name"]
        desc = request.form["description"]
        status = "Not started"
        deadline_str = request.form["deadline"]
        print(f"Deadline string: {deadline_str}")  # Print the deadline string
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except Exception as ex:
            print(f"Error parsing deadline: {ex}")
            return render_template("error.html", message="Error parsing deadline")
        try:
            creator_id = users.user_id()
            print(f"Creator id: {creator_id}")  # Print the creator id
        except Exception as ex:
            print(f"Error getting creator id: {ex}")
            return render_template("error.html", message="Error getting creator id")
        group_id = None
        assignee_id = creator_id
        group_id = None
        if tasks.create_task(name, desc, status, creator_id, assignee_id, group_id, deadline):
            return redirect("/")
    return render_template("error.html", message="Unknown error")

#project_page()
@app.route("/allTasks")
def all_tasks():
    """List all tasks for the user logged in
    Here the user should see all tasks that are assigned to them in all groups
    or the tasks that they has created"""
    task_list = tasks.get_tasks_by_user()
    #projects.refresh_projects(user_projects)
    return render_template('./allTasks.html', tasks=task_list)


#one task page view
@app.route("/task/<int:task_id>")
def task(task_id):
    """Main page for task"""
    task_info = tasks.get_task(task_id)
    #get info about user
    user_info = {'id' : users.user_id(),
                 'name' : users.username(),
                 'role' : users.isleader()}
    print(user_info)
    return render_template('./task.html', task=task_info, date=datetime.now().date(), user=user_info)


@app.route("/error")
def error():
    """Error handler"""
    return render_template("error.html")
