"""User management functions"""
import secrets
from sqlalchemy import text
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(user_name, password):
    """Login handler"""
    sql = text("SELECT id, username, password, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":user_name})
    user = result.fetchone()
    if user is None:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = user.role
        session["csrf_token"] = secrets.token_hex(16)
        return True

    return False

def register(user_name, password, role):
    """Registration handler"""
    sql = text("SELECT 1 FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":user_name})
    if result.fetchone():
        return False

    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password,role) "\
        "VALUES (:username, :password, :role)")
    db.session.execute(sql, {"username":user_name,"password":hash_value,"role":role})
    db.session.commit()
    return login(user_name, password)


def logout():
    """Logout handler"""""
    del session["user_id"]
    del session["username"]
    del session["role"]
    del session["csrf_token"]


def user_id():
    """returns user_id from session"""
    return session.get("user_id", 0)

def username():
    """returns username from session"""
    return session.get("username", 0)

def isleader():
    """returns role from session"""
    return session.get("role", 0)


#def get_user_tasks():
#    """Function to get all tasks for the current user"""
#    sql = text("SELECT * FROM tasks WHERE assignee_id = :user_id")
#    result = db.session.execute(sql, {"user_id": current_user.id})
#    tasks = result.fetchall()
#    return tasks

#def add_uset_to_group(user_id, group_id):
#    """Function to add user to group"""
#    sql = text("INSERT INTO group_users (group_id, user_id) VALUES (:group_id, :user_id)")
#    db.session.execute(sql, {"group_id": group_id, "user_id": user_id})
