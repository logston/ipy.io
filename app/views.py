from flask import Blueprint, render_template

from . import app

bp_container = Blueprint('container', __name__)

@bp_container.route('/')
def index():
    return render_template("base.html")


@bp_container.route('/start-container')
def start_container():
    return render_template('starting_container.html') 

