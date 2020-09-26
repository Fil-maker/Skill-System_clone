import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from api.data import db_session

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

app = Flask(__name__)
db = db_session.global_init()
migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), "data", "migrations"))
api = Api(app)

from api import controllers
