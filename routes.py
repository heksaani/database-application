"""This module contains the routes for the application."""
from datetime import datetime
import secrets
from flask import render_template, request, redirect, session, abort, flash,url_for
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

@app.route("/login", methods=["POST", "GET"])
def login():
    """Login handler"""
    error_input = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            error_input = "Invalid credentials"
    return render_template("index.html", error=error_input)

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

        role = int(request.form["type"])
        status = "user"
        leader = False
        if role == 1:
            status = "leader"
            leader = True

        if users.register(username, password1, leader):
            session["username"] = username
            session["role"] = status
            return redirect(url_for('index'))

        return render_template("error.html", message="Registration failed, username already exists")


    return render_template("error.html", message="Unknown error")

@app.route('/logout', methods=['GET'])
def logout():
    """Logout handler"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('csrf_token', None)
    return redirect(url_for('login'))

@app.route("/createTask", methods=["GET", "POST"])
def create_task():
    """Task creation handler"""
    if request.method == "GET":
        leader_id = users.user_id()
        group_list = list(groups.get_groups(leader_id))
        users_in_groups = {}
        for user_group in group_list:
            users_in_groups[user_group.id] = groups.get_users(user_group.id)
            #users_in_groups[group.id] = groups.get_users(group.id)
        return render_template("createTask.html", groups=group_list, users=users_in_groups)
    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')

        if not user_token or user_token != server_token:
            abort(403)
        name = request.form.get("name")
        desc = request.form.get("description")
        status = "Not started"
        deadline_str = request.form["deadline"]
        group_id = None
        assignee_id = users.user_id()
        group_id = None
        creator_id = users.user_id()
        group_id = request.form.get("group_id") or None

        task_creation_status = tasks.create_task(name, desc, status, creator_id,
                                                 assignee_id, group_id, deadline_str)
        if task_creation_status:
            flash("Task created successfully", "success")
            return redirect(url_for('index'))
        else:
            flash("Failed to create task", "danger")
            return redirect("/createTask")

    return render_template("error.html", message="Unknown error")

@app.route("/assignTask/<int:task_id>", methods=["GET", "POST"])
def assign_task(task_id):
    """Assign task to user in a group.
    This can only be done by the leader of the group."""
    if request.method == "GET":
        users_in_group = groups.get_users(task_id)
        return render_template("assignTask.html", users=users_in_group)
    elif request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        user_id = request.form.get('assignee')
        tasks.set_assigned_time(task_id, user_id)
        return redirect("/task/" + str(task_id))

@app.route("/allTasks")
def all_tasks():
    """List all tasks for the user logged in"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    users_all_tasks = list(tasks.get_tasks_by_user())
    total_tasks = len(users_all_tasks)
    tasks.update_status()

    start = (page - 1) * per_page
    end = start + per_page
    paginated_tasks = users_all_tasks[start:end]

    return render_template('./allTasks.html', tasks=paginated_tasks,
                           total_tasks=total_tasks,
                           per_page=per_page)

@app.route("/task/<int:task_id>", methods=["GET","POST"])
def task(task_id):
    """Main page for task where user can see task name
    and description. If user is leader of the group,
    they can also assign task to other users
    and change the status of the task"""
    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)


        new_status = request.form.get("status")
        if new_status:
            tasks.change_task_status(task_id, new_status)
            return redirect("/task/" + str(task_id))
        action = request.form.get('action')
        if action   == "delete_task":
            print(f"Deleting task with ID {task_id}")
            tasks.delete_task(task_id)
            return redirect("/allTasks")

    task_info = tasks.get_task(task_id)
    user_info = {'id' : users.user_id(),
                 'name' : users.username(),
                 'role' : users.isleader()}
    return render_template('./task.html',task=task_info, date=datetime.now().date(), user=user_info)

@app.route("/editTask/<int:task_id>", methods=["GET","POST"])
def edit_task(task_id):
    try:
        task_to_edit = tasks.get_task(task_id)
        if not task_to_edit:
            return "Task not found", 404

        user_info = {'id': users.user_id(), 'name': users.username(), 'role': users.isleader()}

        if request.method == "GET":
            if task_to_edit['group_id']:
                users_in_group = groups.get_users(task_to_edit['group_id'])
            else:
                users_in_group = []

            return render_template('./editTask.html', task=task_to_edit, user=user_info, users_in_group=users_in_group)

        if request.method == "POST":
            user_token = request.form.get('csrf_token')
            server_token = session.get('csrf_token')
            if not user_token or user_token != server_token:
                abort(403)
            new_name = request.form["task_name"]
            new_description = request.form["task_description"]
            new_deadline = request.form["task_deadline"]
            new_assignee = request.form.get("assignee")


            if new_assignee:
                tasks.set_assigned_time(task_id, new_assignee)
            tasks.edit_task_name(task_id, new_name)
            tasks.edit_description(task_id, new_description)
            tasks.edit_deadline(task_id, new_deadline)
            return redirect("/task/"+str(task_id))
        return render_template("error.html", message="Unknown error")
    except Exception as e:
        return render_template("error.html", message=str(e))





@app.route("/createGroup", methods=["GET", "POST"])
def create_group():
    """Group creation handler
    where leader can create a group and add members to it"""

    if request.method == "GET":
        leader_groups = list(groups.get_groups(users.user_id()))
        all_users = list(users.get_all_users())
        return render_template("createGroup.html", leader_groups=leader_groups, all_users=all_users)

    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)

        # First we create the group
        if 'group_name' in request.form:
            group_name = request.form["group_name"]
            leader_id = users.user_id()
            if groups.create_group(group_name, leader_id):
                flash("Group created successfully", 'success')
            else:
                flash("Group creation failed", 'error')

        # Add members to the group
        elif 'group_id' in request.form and 'members' in request.form:
            group_id = request.form["group_id"]
            members = request.form.getlist("members")

            for user_id in members:
                groups.add_user_to_group(user_id, group_id)

        # Refresh the list of groups and users
        leader_groups = list(groups.get_groups(users.user_id()))
        all_users = list(users.get_all_users())

        return render_template("createGroup.html", leader_groups=leader_groups, all_users=all_users)


@app.route("/allGroups")
def all_groups():
    """List all groups for the user logged in"""
    page = request.args.get('page', 1, type=int)
    per_page = 10

    user_id = users.user_id()
    users_all_groups = list(groups.get_groups(user_id))

    total_groups= len(users_all_groups)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_groups= users_all_groups[start:end]

    return render_template('./allGroups.html', groups=paginated_groups,
                           total_groups=total_groups,
                           per_page=per_page)

@app.route("/group/<int:group_id>", methods=["GET", "POST"])
def group(group_id):
    """Main page for group
    List all groups for the user logged in"""
    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        action = request.form.get('action')

        if action == "delete_group":
            groups.delete_group(group_id)
            return redirect("/allGroups")
        elif action == "edit_group":
            return redirect("/editGroup/"+str(group_id))
        elif action == "add_user":
            return redirect("/assignTask/"+str(group_id))

    group_info = list(groups.get_group(group_id))
    group_members = list(groups.get_users(group_id))
    group_tasks = list(tasks.get_tasks_by_group(group_id))
    group_id = group_info[0].id
    time_spent=tasks.get_time_for_task(group_id)

    return render_template('./group.html', group=group_info,
                           members=group_members,
                           tasks=group_tasks,
                           time_spent=time_spent)

@app.route("/editGroup/<int:group_id>", methods=["GET", "POST"])
def edit_group(group_id):
    """Edit group page where user can edit group name
    and description "
    So always the creator of the group can edit it"""

    group_to_edit = groups.get_group(group_id)
    if not group_to_edit:
        return "Group not found", 404

    if request.method == "GET":
        return render_template('./editGroup.html', task=group_to_edit)

    if request.method == "POST":
        user_token = request.form.get('csrf_token')
        server_token = session.get('csrf_token')
        if not user_token or user_token != server_token:
            abort(403)
        new_name = request.form["group_name"]
        groups.edit_group_name(group_id, new_name)

    return render_template("error.html", message="Unknown error")


@app.route("/addUser", methods=["GET", "POST"])
def add_user():
    """Add user to group on separate page"""
    all_users = users.get_all_users()
    leader_id = users.user_id()
    users_all_groups = groups.get_groups(leader_id)

    if request.method == "POST":
        user_id = request.form.get("user")
        group_id = request.form.get("group")
        if groups.add_user_to_group(user_id, group_id):  
            flash("User added successfully", 'success')
        else:
            flash("User addition failed", 'error')
    return render_template("addUser.html", users=all_users, groups=users_all_groups)




@app.route("/error")
def error():
    """Error handler"""
    return render_template("error.html")
