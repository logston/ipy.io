from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.security import AnonymousUser, Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from .models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

mail = Mail(app)

from app.views import bp_container
app.register_blueprint(bp_container)

