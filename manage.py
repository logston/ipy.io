import docker
from flask.ext.script import Manager

from app import app


manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=True, port=8888)


@manager.command
def kill_all_containers():
    print('Collecting containers ... ')
    client = docker.Client(base_url=app.config['DOCKER_HOST'])
    containers = client.containers()

    if not containers:
        print('No containers found.')

    for i, container in enumerate(containers, start=1):
        print('Killing container {} ({}/{}) ... '
              ''.format(container['Id'], i, len(containers)), end='')
        client.stop(container['Id'])
        print('Done.')


if __name__ == '__main__':
    manager.run()

