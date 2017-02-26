""" Login Handler """
from handlers import BaseHandler
from models import User


class Login(BaseHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'That username and password combo is invalid'
            self.render('login-form.html', error=msg)
