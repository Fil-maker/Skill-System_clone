import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from api.data import db_session

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

api = Api(app)

db_session.global_init()

from api import controllers
