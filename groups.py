"""Functions to handle groups."""
from sqlalchemy import text
#from flask import session
from db import db
#import users


def create_group(group_name, leader_id):
    """Group creation handler"""
    sql = text("INSERT INTO groups (name, leader_id) "\
               "VALUES (:name, :leader_id) RETURNING id")
    result = db.session.execute(sql, {"name": group_name, "leader_id": leader_id})
    group_id = result.fetchone()[0]
    sql_group = text("INSERT INTO usergroups (user_id, group_id) "\
                     "VALUES (:user_id, :group_id)")
    db.session.execute(sql_group, {"user_id": leader_id, "group_id": group_id})
    db.session.commit()
    return True

def add_user_to_group(user_id, group_id):
    """Function to add user to group"""
    sql = text("INSERT INTO usergroups (user_id, group_id) "\
               "VALUES (:user_id, :group_id)")
    db.session.execute(sql, {"user_id": user_id, "group_id": group_id})
    db.session.commit()
    return True


def get_groups(user_id):
    """Function to get ALL groups by user_id"""
    sql = text("SELECT G.id, G.name FROM Groups G " \
           "WHERE G.leader_id = :user_id " \
           "ORDER BY G.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result

def get_users(group_id):
    """Function to get all users in group"""
    sql = text("SELECT U.id, U.username FROM Users U " \
           "JOIN UserGroups UG ON U.id = UG.user_id " \
           "WHERE UG.group_id = :group_id " \
           "ORDER BY U.id")
    result = db.session.execute(sql, {"group_id": group_id})
    return result

def get_group(group_id):
    """Function to get group by group_id"""
    sql = text("SELECT G.id, G.name FROM Groups G " \
           "WHERE G.id = :group_id " \
           "ORDER BY G.id")
    result = db.session.execute(sql, {"group_id": group_id})
    return result

def edit_group_name(group_id, name):
    """Function to edit group name"""
    sql = text("UPDATE Groups SET name=:name WHERE id=:group_id")
    db.session.execute(sql, {"group_id": group_id, "name": name})
    db.session.commit()
    return True

def delete_group(group_id):
    """Function to delete group"""
    sql = text("DELETE FROM Groups WHERE id=:group_id")
    db.session.execute(sql, {"group_id": group_id})
    db.session.commit()
    return True
