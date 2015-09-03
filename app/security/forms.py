import re

from flask import request
from flask.ext.security.forms import (
    ConfirmRegisterForm, NextFormMixin, Required, 
    get_form_field_label, ValidatorMixin
)
from flask.ext.security.utils import get_message, url_for_security
from wtforms import StringField, ValidationError

from ..models import User


class Subdomain(ValidatorMixin):
    valid_pattern = re.compile('^[\w_-]+$')

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if not self.valid_pattern.match(field.data):
            raise ValidationError(self.message)
        

subdomain_required = Required(message='SUBDOMAIN_NOT_PROVIDED')
subdomain_validator = Subdomain(message='INVALID_SUBDOMAIN')


def unique_user_subdomain(form, field):
    if User.query.filter_by(subdomain=field.data).first():
        msg = get_message('SUBDOMAIN_ALREADY_ASSOCIATED', subdomain=field.data)[0]
        raise ValidationError(msg)


class RegisterForm(ConfirmRegisterForm, NextFormMixin):
    subdomain = StringField(
        'Subdomain',
        validators=[subdomain_required, subdomain_validator, unique_user_subdomain])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get('next', url_for_security('login'))

