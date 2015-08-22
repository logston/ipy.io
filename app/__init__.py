from flask import Flask
app = Flask(__name__)

app.config.from_object('config')

from app.views import mod as coreModule
app.register_blueprint(coreModule)

