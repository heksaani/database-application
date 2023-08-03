from flask import Flask
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')

import routes
