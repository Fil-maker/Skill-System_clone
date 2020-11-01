import os

from dotenv import load_dotenv
from flask import Flask
from .momentjs import momentjs

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("APP_SECRET")
app.jinja_env.globals["momentjs"] = momentjs

from app import controllers
