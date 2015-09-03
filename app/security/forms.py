from flask import request
from flask.ext.security.forms import ConfirmRegisterForm, NextFormMixin


class RegisterForm(ConfirmRegisterForm, NextFormMixin):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        if not self.next.data:
            self.next.data = request.args.get('next', '')

