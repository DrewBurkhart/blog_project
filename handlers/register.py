import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from signup import Signup
from models import *
from string import letters
from google.appengine.ext import db


class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'Name taken. Someone else beat you to it.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')
