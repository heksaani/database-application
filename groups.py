"""Functions to handle groups."""
from db import db
from flask import session
from sqlalchemy import text
import users


def get_groups(user_id):
    """Function to get ALL groups by user_id"""
    sql = text("SELECT G.id, G.name FROM Groups G " \
           "WHERE G.leader_id = :user_id " \
           "ORDER BY G.id")
    result = db.session.execute(sql, {"user_id": user_id})
    return result
