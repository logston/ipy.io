from flask.ext.security import UserMixin, RoleMixin

from . import db


roles_users = db.Table(
    'roles_users',
     db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
     db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Role {}/{}>'.format(self.id, self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    subdomain = db.Column(db.String(255), unique=True)
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(45))
    current_login_ip = db.Column(db.String(45))
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}/{}>'.format(self.id, self.email)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship('User',
       			      backref=db.backref('groups', lazy='dynamic'))
    delete_ts = db.Column(db.DateTime)
    file_path = db.Column(db.String(255))
    max_containers = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Group {}/{}>'.format(self.id, self.name)


class Container(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', 
                            backref=db.backref('containers', lazy='dynamic'))
    container_id = db.Column(db.String(64), unique=True)

    def __init__(self, group_id, container_id):
        self.group_id = group_id
        self.container_id = container_id
    
    def __repr__(self):
        return '<Container {}/Group {}/Container {}>'.format(self.id,
                        				     self.group,
 							     self.container_id[:7])

