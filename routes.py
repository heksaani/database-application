"""This module contains the routes for the application."""
from datetime import datetime
import secrets
from flask import render_template, request, redirect, session, abort
import users
import tasks
import groups
from app import app

@app.before_request
def make_csrf_token():
    """Create CSRF token"""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)


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
        user_token = request.form["csrf_token"]
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Invalid username or password")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Registration handler"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":

        user_token = request.form["csrf_token"]
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="Passwords do not match")
        if password1 == "" or username == "":
            return render_template("error.html", message="Password cannot be empty")
        if len(password1) < 8 or len(password1) > 20:
            return render_template("error.html", message="Password must be between 8 and 20 characters")
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Username must be between 3 and 20 characters")
        
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

@app.route("/createTask", methods=["GET", "POST"])
def create_task():
    """Task creation handler"""
    if request.method == "GET":
        leader_id = users.user_id()
        group_list = list(groups.get_groups(leader_id))
        users_in_groups = {}
        for group in group_list:
            users_in_groups[group.id] = groups.get_users(group.id)
        return render_template("createTask.html", groups=group_list, users=users_in_groups)
    
    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')

        if not user_token or user_token != server_token:
            abort(403)
        name = request.form["name"]
        desc = request.form["description"]
        status = "Not started"
        deadline_str = request.form["deadline"]
        group_id = None
        assignee_id = users.user_id()
        group_id = None
        creator_id = users.user_id()

        if tasks.create_task(name, desc, status, creator_id, assignee_id, group_id, deadline_str):
            return redirect("/")
    return render_template("error.html", message="Unknown error")

@app.route("/assignTask/<int:group_id>", methods=["GET", "POST"])
def assign_task(group_id):
    """Assign task to user in group
    this can be only done by the leader of the group"""
    if request.method == "GET":
        users_in_group = groups.get_users(group_id)
        render_template("assignTask.html", users=users_in_group)
    elif request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        return

@app.route("/allTasks")
def all_tasks():
    """List all tasks for the user logged in
    Here the user should see all tasks that are assigned to them in all groups
    or the tasks that they has created"""
    task_list = list(tasks.get_tasks_by_user())
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
    return render_template('./task.html',task=task_info, date=datetime.now().date(), user=user_info)

#edit task page view
@app.route("/editTask/<int:task_id>", methods=["GET"])
def edit_task(task_id):
    """Edit task page"""
    task_to_edit = tasks.get_task(task_id)
    if not task:
        return "Task not found", 404
    task_to_edit.name = request.form['task_name']
    task_to_edit.description = request.form['task_description']

    # Check if current user is the creator before updating the deadline
    if task.creator_id == session['user_id']:
        task.deadline = request.form['deadline']
    return redirect(('allTasks'))

@app.route("/createGroup", methods=["GET", "POST"])
def create_group():
    """Group creation handler"""
    if request.method == "GET":
        return render_template("createGroup.html")
    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        group_name = request.form["group_name"]
        leader_id = users.user_id()
        if groups.create_group(group_name, leader_id):
            return render_template("index.html")
        else:
            return render_template("error.html", message="Group creation failed")

@app.route("/allGroups")
def all_groups():
    """List all groups for the user logged in"""
    user_id = users.user_id()
    group_list = list(groups.get_groups(user_id))
    return render_template('./allGroups.html', groups=group_list)

@app.route("/error")
def error():
    """Error handler"""
    return render_template("error.html")
