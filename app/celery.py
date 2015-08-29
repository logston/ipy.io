import os
import random
import time

from celery import Celery
import docker

from . import app
from .utils import EPHEMERAL_PORT_RANGE


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


celery = make_celery(app)


@celery.task
def start_container(group_id):
    """
    :return: url of container
    :rtype: str
    """
    client = docker.Client(base_url=app.config['DOCKER_HOST'])

    # Get group
    # check if has been stopped or is past its time allotment
    # check if group has already hit max containers
    # check if group's file is already in place in temp dir
    # pull file from cdn and place in group's temp dir

    image = app.config['DOCKER_IMAGE']
    notebook_dir = app.config['NOTEBOOK_DIR']
    group_file = '/tmp/PgBouncerTimingTests.ipynb'
    docker_read_only_file = os.path.join(notebook_dir, os.path.basename(group_file))
    command = 'sh -c "jupyter notebook --notebook-dir={}"'.format(notebook_dir)
    host_port = random.randint(*EPHEMERAL_PORT_RANGE)
    create_container_params = {
        'image': image,
        'command': command,
        'volumes': [docker_read_only_file],
        'ports': [8888],   # Open port for business
        'host_config': docker.utils.create_host_config(
            binds={
                group_file: {
                    'bind': docker_read_only_file,
                    'mode': 'ro',
                }
            },  
            port_bindings={8888: host_port}
        ),
    } 

    container = client.create_container(**create_container_params)
    container_id = container.get('Id')

    # save container id to group/container table

    client.start(container=container_id)

    time.sleep(1)  # hack to avoid 404's while container starts

    # get group.creator.subdomain

    url_parts = {
        'scheme': app.config['SCHEME'],
        'subdomain': 'test',
        'domain': app.config['DOMAIN'],
        'port': host_port
    } 
    return '{scheme}://{subdomain}.{domain}:{port}'.format(**url_parts)

