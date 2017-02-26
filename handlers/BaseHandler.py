""" Base Handler for others handlers to import from """
import os
import random
import hashlib
import hmac
from string import letters
import webapp2
import jinja2
from models import User
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    """ Define the render string function """
    t = jinja_env.get_template(template)
    return t.render(params)

# used for hashing password by making a salt and applying it to pw
def make_salt(length=5):
    """ Make salt for hashing """
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt=None):
    """ Use salt to make hash """
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    """ Define valid password """
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group='default'):
    """ Create the users_key """
    return db.Key.from_path('users', group)

# Functions for hashing and passwords
secret = 'ie7dj^uejd(92due63ye^&uejd7364@'

def make_secure_val(val):
    """ Create a secure value """
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    """ Check that secure value """
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val

class BaseHandler(webapp2.RequestHandler):
    """ Main BaseHandler class that other classes will inherit from """
    def write(self, *a, **kw):
        """ Makes it so you don't have to write response.out. every time """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """ Define the render string function """
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        """ Define the render function """
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """ Set a secure cookie for the user """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """ Read the secure cookie we have set """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """ Define the login function """
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """ Define the logout function """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """ define self.user """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
