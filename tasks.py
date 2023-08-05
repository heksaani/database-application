"""Functions to handle tasks."""
from sqlalchemy import text
from db import db
import users

def task(task_id):
    "Get task by id"
    sql = "SELECT name, description FROM Tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":task_id})
    return result.fetchone()

def create_task(name, description, status, deadline):
    """Function to create a new task"""
    sql = text("INSERT INTO tasks (name, description, status, deadline, assignee_id) "\
            "VALUES (:name, :description, :status, :deadline, :assignee_id) RETURNING id")
    result = db.session.execute(sql, {"name": name, "description": description, "status": status, "deadline": deadline, "assignee_id": current_user.id})
    db.session.commit()
