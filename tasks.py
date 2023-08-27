"""Functions to handle tasks."""
import datetime
from sqlalchemy import text
#from flask import session
import users
from db import db
#import users

def create_task(name, description, status, creator_id, assignee_id, group_id, deadline):
    """Function to create a new task"""
    sql = text("INSERT INTO tasks (name, description, status, creator_id, assignee_id, "
               "group_id, deadline) VALUES (:name, :description, :status, :creator_id, "
               ":assignee_id, :group_id, :deadline)")

    db.session.execute(
        sql,{
            "name": name,
            "description": description,
            "status": status,
            "creator_id": creator_id,
            "assignee_id": assignee_id,
            "group_id": group_id,
            "deadline": deadline
        })
    db.session.commit()
    return True

def get_tasks_by_user():
    """Function to get ALL tasks by user"""
    user_id = users.user_id()
    sql = text("SELECT T.id, T.name FROM Tasks T " \
           "WHERE T.creator_id = :user_id OR T.assignee_id = :user_id " \
           "ORDER BY T.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result


def get_task(task_id):
    """Getting one task by task id"""
    sql = text("SELECT * FROM Tasks WHERE id=:task_id")
    result = db.session.execute(sql, {"task_id": task_id})
    task_result = result.fetchone()
    #task results as dictionary:
    task_dict = {'id': task_result[0],
                    'name': task_result[1],
                    'description': task_result[2],
                    'status': task_result[3],
                    'creator_id': task_result[4],
                    'assignee_id': task_result[5],
                    'group_id': task_result[6],
                    'deadline': task_result[7]
                    }
    return task_dict

def edit_task_name(task_id, name):
    """Function to edit task name"""
    sql = text("UPDATE Tasks SET name=:name WHERE id=:task_id")
    db.session.execute(sql, {"task_id": task_id, "name": name})
    db.session.commit()
    return True

def edit_description(task_id, description):
    """Function to edit task description"""
    sql = text("UPDATE Tasks SET description=:description WHERE id=:task_id")
    db.session.execute(sql, {"task_id": task_id, "description": description})
    db.session.commit()
    return True

def task_name(task_id):
    '''Get task name by id'''
    sql = text("SELECT name FROM Tasks WHERE id=:task_id")
    result = db.session.execute(sql, {"task_id":task_id})
    return result.fetchone()[0]

def update_status():
    """Function to update tasks status badsed on their deadline"""
    current_time = datetime.datetime.now()
    sql = text("UPDATE Tasks SET status='Late' WHERE deadline < :current_time")
    db.session.execute(sql, {"current_time": current_time})
    db.session.commit()




#leader functions
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
