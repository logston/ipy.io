import docker
from flask.ext.script import Manager

from app import app, db, user_datastore


manager = Manager(app)


def get_and_validate(field_name, is_bool=False):
    value = '' 
    while not value:
        value = input('{} >> '.format(field_name)).strip()
        if is_bool:
            value = value.lower()
            if value not in ('true', 'false'):
                print('Please enter True or False')
                value = ''
            else:
                return value == 'true'
    return value


@manager.command
def runserver():
    app.run(debug=True, port=8888)


@manager.command
def create_db():
    print('Creating db ... ', end='')
    db.create_all()
    user_datastore.find_or_create_role(name='admin', description='Administrator')
    db.session.commit()
    print('Done.')


@manager.command
def create_user():
    print("Let's create a new user ... ")
    email = get_and_validate('email')
    password = get_and_validate('password')
    active = get_and_validate('active (True/False)', is_bool=True)
    admin = get_and_validate('admin (True/False)', is_bool=True)
    if not user_datastore.get_user(email):
        user_datastore.create_user(email=email, password=password, active=active)
    else:
        print('User by email {} already exists.'.format(email))
    if admin:
        user_datastore.add_role_to_user(email, 'admin')
    db.session.commit()


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

