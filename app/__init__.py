from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
DB = SQLAlchemy(app)
migrate = Migrate(app, DB)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_first_request
def create_table():
    DB.create_all()

from app import routes, models
