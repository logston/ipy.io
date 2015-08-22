from flask import Blueprint, render_template

from . import app

mod = Blueprint('core', __name__, url_prefix='/core')

@mod.route('/')
def index():
    return render_template("base.html")


@mod.route('/start-container', methods=['GET', 'POST'])
def start_container():
    return render_template('starting_container.html') 

