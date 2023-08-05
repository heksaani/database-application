"""This is the main file for the application."""
from os import getenv
from flask import Flask
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
import routes