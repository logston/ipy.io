from celery import Celery
from docker import Client

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
    client = Client(base_url='unix://var/run/docker.sock')
    container = client.create_container(image='logston/notebook:0.1.3', 
                                        command='sh -c "jupyter notebook --notebook-dir=/srv"')
    client.start(container=container.get('Id'))
    ports = client.port(container.get('Id'), 8888)
    host_port = ports[0]['HostPort']
   
    return 'http://ipy.vg:{}'.format(host_port)

