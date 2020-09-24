import os

from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

app = Flask(__name__)

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

api = Api(app)

from api import controllers
