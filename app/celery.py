import os
import random
import time

from celery import Celery
import docker

from . import app
from .models import Group
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

    group = Group.query.get(group_id)
    if group.stopped_ts:
        return 'url_for_closed group'

    if len(group.containers) >= group.max_containers:
        return 'max containers reached'
    
    if not os.path.exists(group.file_path):
        # pull file from cdn and place in group's temp dir
        pass

    image = app.config['DOCKER_IMAGE']
    notebook_dir = app.config['NOTEBOOK_DIR']
    docker_read_only_file = os.path.join(notebook_dir, 
                                         os.path.basename(group.file_path))
    command = 'sh -c "jupyter notebook --notebook-dir={}"'.format(notebook_dir)
    host_port = random.randint(*EPHEMERAL_PORT_RANGE)
    create_container_params = {
        'image': image,
        'command': command,
        'volumes': [docker_read_only_file],
        'ports': [8888],   # Open port for business
        'host_config': docker.utils.create_host_config(
            binds={
                group.file_path: {
                    'bind': docker_read_only_file,
                    'mode': 'ro',
                }
            },  
            port_bindings={8888: host_port}
        ),
    } 

    container = client.create_container(**create_container_params)
    container_id = container.get('Id')

    db.session.add(Container(group.id, container_id))
    db.session.commit()

    client.start(container=container_id)

    time.sleep(1)  # hack to avoid 404's while container starts

    url_parts = {
        'scheme': app.config['SCHEME'],
        'subdomain': group.creator.subdomain,
        'domain': app.config['DOMAIN'],
        'port': host_port
    } 
    return '{scheme}://{subdomain}.{domain}:{port}'.format(**url_parts)

