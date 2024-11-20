"""
This module sets up the Flask application, configures it, initializes the database and session,
and includes the logic to create all necessary database tables upon the first request.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

DB = SQLAlchemy(app)
migrate = Migrate(app, DB)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.before_first_request
def create_table():
    """
    Creates all database tables defined in the application models
    before the first request is processed.
    """
    DB.create_all()


# Ignore Pylint warning for import position
from app import routes, models  # pylint: disable=wrong-import-position

# If you want to make the app run on development mode, debug=True will be helpful
# export FLASK_ENV=development
# export FLASK_DEBUG=1