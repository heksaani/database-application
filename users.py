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

def user_id():
    """returns user_id from session"""
    return session.get("user_id", 0)

def username():
    """returns username from session"""
    return session.get("username", 0)

def isleader():
    """returns role from session"""
    return session.get("role", 0)

def get_all_users():
    """Function to get ALL users"""
    sql = text("SELECT U.id, U.username FROM Users U " \
           "ORDER BY U.id")
    result = db.session.execute(sql)
    return result
