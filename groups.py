"""Functions to handle groups."""
from sqlalchemy import text
#from flask import session
from db import db
#import users


def create_group(group_name, leader_id):
    """Group creation handler"""
    sql = text("INSERT INTO groups (name, leader_id) "\
        "VALUES (:name, :leader_id)")
    db.session.execute(sql, {"name":group_name,"leader_id":leader_id})
    db.session.commit()
    return True