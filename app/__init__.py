import os

from dotenv import load_dotenv
from flask import Flask
from app.jinja import momentjs, text, get_env

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("APP_SECRET")
app.jinja_env.globals["momentjs"] = momentjs
app.jinja_env.globals["text"] = text
app.jinja_env.filters["get_env"] = get_env

from app import controllers
from app.ajax_controllers import ajax

app.register_blueprint(ajax, url_prefix='/ajax')
