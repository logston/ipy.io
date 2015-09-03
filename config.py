import os


basedir = os.path.abspath(os.path.dirname(__file__))


SCHEME = 'http'
DOMAIN = 'ipy.vg'

CELERY_BROKER_URL='redis://localhost:6379',
CELERY_RESULT_BACKEND='redis://localhost:6379'

DOCKER_HOST='unix:///var/run/docker.sock'
DOCKER_IMAGE = 'logston/notebook:0.1.3'

NOTEBOOK_DIR = '/home/'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SECRET_KEY = 'the-most-secret-thing-ever-more-secret-than-moon-people'

SECURITY_RECOVERABLE = True
SECURITY_REGISTERABLE = True
SECURITY_CONFIRM_URL = False

MAIL_SERVER = 'smtp.example.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'username'
MAIL_PASSWORD = 'password'

