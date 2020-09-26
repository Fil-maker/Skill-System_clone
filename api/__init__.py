import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from api.data import db_session
from api.resources.users import UserResource, UserListResource

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("API_SECRET")
pg_user = os.environ.get("PG_USER")
pg_pass = os.environ.get("PG_PASS")
pg_host = os.environ.get("PG_HOST")
db_name = os.environ.get("DB_NAME")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://{pg_user}:{pg_pass}@{pg_host}/{db_name}"

db = db_session.global_init()
db.init_app(app)
migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), "data", "migrations"))
api = Api(app)

api.add_resource(UserResource, "/api/users/<int:user_id>")
api.add_resource(UserListResource, "/api/users")

from api import controllers
