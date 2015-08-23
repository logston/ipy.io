from flask import Flask
app = Flask(__name__)

app.config.from_object('config')

from app.views import bp_container
app.register_blueprint(bp_container)

