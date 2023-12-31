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

def change_task_status(task_id, new_status):
    """Update the status of a task by using a button and task id"""
    sql = text("UPDATE Tasks SET status=:new_status WHERE id=:task_id")
    db.session.execute(sql, {"new_status": new_status, "task_id": task_id})
    db.session.commit()

def edit_deadline(task_id, deadline):
    """Function to edit task deadline"""
    sql = text("UPDATE Tasks SET deadline=:deadline WHERE id=:task_id")
    db.session.execute(sql, {"task_id": task_id, "deadline": deadline})
    db.session.commit()
    return True

def update_status():
    """Function to update tasks status badsed on their deadline"""
    current_time = datetime.datetime.now()
    sql = text("UPDATE Tasks SET status='Late' WHERE deadline < :current_time")
    db.session.execute(sql, {"current_time": current_time})
    db.session.commit()

def delete_task(task_id):
    """Function to delete a task"""
    print(f"Deleting task with ID {task_id}")
    sql = text("DELETE FROM Tasks WHERE id=:task_id")
    db.session.execute(sql, {"task_id": task_id})
    db.session.commit()
    return True

def get_all_tasks(user_id):
    """Function to get ALL tasks by user_id"""
    sql = text("SELECT T.id, T.name FROM Tasks T " \
           "WHERE T.creator_id = :user_id OR T.assignee_id = :user_id " \
           "ORDER BY T.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result

def get_tasks_by_group(group_id):
    """Function to get ALL tasks by group_id"""
    sql = text("SELECT T.id, T.name FROM Tasks T " \
           "WHERE T.group_id = :group_id " \
           "ORDER BY T.id")
    result = db.session.execute(sql, {"group_id": group_id})
    return result

def get_time_for_task(group_id):
    """Function to return a dictionary of task_id: time_spent for a group"""
    query = text("""SELECT task_id, SUM(time_spent)
                    FROM TaskTime 
                    WHERE task_id IN (SELECT id FROM Tasks WHERE group_id = :group_id) 
                    GROUP BY task_id""")

    result = db.session.execute(query, {'group_id': group_id})  # Changed this line

    result_dict = {}
    for row in result:
        result_dict[row[0]] = row[1]
    return result_dict

def update_time_spent(task_id, user_id):
    """Function to update time spent on a task"""
    query = text("""UPDATE TaskTime SET time_spent = NOW() - assigned_at
                     WHERE task_id = :task_id AND user_id = :user_id""")
    db.session.execute(query, {'task_id': task_id, 'user_id': user_id})
    db.session.commit()

def set_assigned_time(task_id, user_id):
    """Function to set time spent on a task"""
    query = text("""INSERT INTO TaskTime (task_id, user_id, assigned_at)
                 VALUES (:task_id, :user_id, NOW())""")
    db.session.execute(query, {'task_id': task_id, 'user_id': user_id})
    db.session.commit()

def assign_task_to_user(task_id, user_id):
    """Assigns a task to a user by updating the assignee_id field in the Tasks table."""
    sql = text("UPDATE Tasks SET assignee_id=:user_id WHERE id=:task_id")
    db.session.execute(sql, {"user_id": user_id, "task_id": task_id})
    db.session.commit()
