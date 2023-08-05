"""Functions to handle tasks."""
from sqlalchemy import text
from db import db
#import users

def task(task_id):
    "Get task by id"
    sql = "SELECT name, description FROM Tasks WHERE id=:id"
    result = db.session.execute(sql, {"id":task_id})
    return result.fetchone()

def create_task(name, description, status, creator_id, assignee_id, group_id, deadline):
    """Function to create a new task"""
    sql = text("INSERT INTO tasks (name, description, status, creator_id, assignee_id, group_id, deadline) VALUES (:name, :description, :status, :creator_id, :assignee_id, :group_id, :deadline)")
    try:
        db.session.execute(sql, {"name":name, "description":description, "status":status, "creator_id":creator_id, "assignee_id":assignee_id, "group_id":group_id, "deadline":deadline})
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error creating task: {e}")
        return False


#def add_user_to_group(user_id, group_id):
#    """Function to add user to group"""
#    sql = text("INSERT INTO group_users (group_id, user_id) VALUES (:group_id, :user_id)")
#    db.session.execute(sql, {"group_id": group_id, "user_id": user_id})
#    db.session.commit()
#    return True

#def add_task_to_group(task_id, group_id):
#    """Function to add task to group"""
#    sql = text("INSERT INTO group_tasks (group_id, task_id) VALUES (:group_id, :task_id)")
#    db.session.execute(sql, {"group_id": group_id, "task_id": task_id})
#    db.session.commit()
#    return True

#deleting task
#def delete_task(task_id):
#    """Function to delete a task"""
#    sql = text("DELETE FROM tasks WHERE id=:id")
#    db.session.execute(sql, {"id":task_id})
#    db.session.commit()
