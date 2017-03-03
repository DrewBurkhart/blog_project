""" Signup Handler """
import re
from handlers import BaseHandler


# Defining the constraints for our username, pw and email addresses
def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)


def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)


def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)


class Signup(BaseHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        has_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.reenter = self.request.get('reenter')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "Invalid username"
            has_error = True

        if not valid_password(self.password):
            params['error_password'] = "Invalid password"
            has_error = True

        elif self.password != self.reenter:
            params['error_reenter'] = "Your passwords didn't match."
            has_error = True

        if not valid_email(self.email):
            params['error_email'] = "Invalid email"
            has_error = True

        if has_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
