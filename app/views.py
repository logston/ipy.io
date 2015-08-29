from flask import Blueprint, render_template, jsonify

from . import app
from .celery import start_container as async_start_container

bp_container = Blueprint('container', __name__)

@bp_container.route('/')
def index():
    return render_template("base.html")


@bp_container.route('/start-container')
def start_container():
    user_id = 1
    group_id = 1

    async_result = async_start_container.delay(group_id, user_id)

    context = {'async_result_id': async_result.id}

    return render_template('starting_container.html', **context)


@bp_container.route('/container-startup-status/<async_result_id>')
def container_startup_status(async_result_id):
    async_result = async_start_container.AsyncResult(async_result_id)

    if async_result.status == 'FAILURE':
        return jsonify({'href': '/container-start-failure'})
      
    if async_result.status == 'SUCCESS':
        return jsonify({'href': async_result.result})

    return jsonify({'href': False})


@bp_container.route('/container-start-failure')
def container_start_failure():
    return render_template('container_start_failure.html')

