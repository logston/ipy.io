from celery import Celery
import docker

from . import app


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
def start_container(group_id, user_id):
    """
    :return: url of container
    :rtype: str
    """
    client = docker.Client(base_url=app.config['DOCKER_HOST'])
    create_container_params = {
        'image': 'logston/notebook:0.1.3',
        'command': 'sh -c "jupyter notebook --notebook-dir=/srv"',
        'ports': [8888],   # Open port for business
        'host_config': docker.utils.create_host_config(
        	port_bindings={8888: 49827}
        ),
    } 
    container = client.create_container(**create_container_params)
    container_id = container.get('Id')
    response = client.start(container=container_id)
   
    return 'http://ipy.vg:{}'.format(49827)

