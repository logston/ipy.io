from flask import Blueprint, render_template, jsonify

from . import app

bp_container = Blueprint('container', __name__)

@bp_container.route('/')
def index():
    return render_template("base.html")


@bp_container.route('/start-container')
def start_container():
    context = {
        'async_result_id': 1
    }
    return render_template('starting_container.html', **context)


@bp_container.route('/container-startup-status/<async_result_id>')
def container_startup_status(async_result_id):
    # get celery task status   
    import random 
      
    done = False if random.random() > 0.2 else True
 
    # if task is not done
    if not done:
        return jsonify({'href': False})

    return jsonify({'href': 'http://plog.logston.me'})

