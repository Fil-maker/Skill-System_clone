import os

from dotenv import load_dotenv
from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restful import Api

from api.data import db_session
from api.resources.events import EventResource, EventListResource, EventParticipantResource
from api.resources.users import UserResource, UserListResource, UserPinResource, \
    UsersEventListResource

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    raise FileNotFoundError(".env file not found")

app = Flask(__name__)
pg_user = os.environ.get("PG_USER")
pg_pass = os.environ.get("PG_PASS")
pg_host = os.environ.get("PG_HOST")
db_name = os.environ.get("DB_NAME")
app.config["SECRET_KEY"] = os.environ.get("API_SECRET")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://{pg_user}:{pg_pass}@{pg_host}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")

db = db_session.global_init()
db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), "data", "migrations"))
api = Api(app)

api.add_resource(UserResource, "/api/users/<int:user_id>")
api.add_resource(UserListResource, "/api/users")
api.add_resource(UserPinResource, "/api/users/<int:user_id>/pin")
api.add_resource(UsersEventListResource, "/api/users/<int:user_id>/events")

api.add_resource(EventResource, "/api/events/<int:event_id>")
api.add_resource(EventListResource, "/api/events")
api.add_resource(EventParticipantResource, "/api/events/<int:event_id>/participants")

from api import controllers
