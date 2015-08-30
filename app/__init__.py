from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from .models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


from app.views import bp_container
app.register_blueprint(bp_container)

