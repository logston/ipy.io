import os


basedir = os.path.abspath(os.path.dirname(__file__))


SCHEME = 'http'
DOMAIN = 'ipy.vg'

CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'

DOCKER_HOST='unix:///var/run/docker.sock'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

