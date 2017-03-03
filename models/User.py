""" Create user class """
import random
import hashlib
import hmac
import webapp2
from string import letters
from google.appengine.ext import db


def make_salt(length=5):
    """ Used for hashing password by making a salt and applying it to pw """
    return ''.join(random.choice(letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """ Make hash for password """
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)


def valid_pw(name, password, h):
    """ Define valid password """
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)


def users_key(group='default'):
    """ Create the users key """
    return db.Key.from_path('users', group)


secret = 'ie7dj^uejd(92due63ye^&uejd7364@'


def make_secure_val(val):
    """ Make a secure value """
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())


def check_secure_val(secure_val):
    """ Check the secure value """
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


class UserHandler(webapp2.RequestHandler):
    """ Main UserHandler class that other classes will inherit from """
    def write(self, *a, **kw):
        """ Makes it so you don't have to write response.out. every time """
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        """ Define the redner string function """
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        """ Define the render function """
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        """ Set the secure cookie value """
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        """ Read the secure cookie for the user """
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        """ Define the login function """
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        """ Define the logout function """
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        """ Define the self.user """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))


# User

# Defines User class and creates methods
# to retrieve users and their info
class User(db.Model):
    """ Create the user class """
    name = db.StringProperty(required=True)
    pw_hash = db.StringProperty(required=True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        """ Find user by id """
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        """ Find user by name """
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email=None):
        """ Register a user """
        pw_hash = make_pw_hash(name, pw)
        return cls(parent=users_key(),
                   name=name,
                   pw_hash=pw_hash,
                   email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


class Login(UserHandler):
    """ Create the login class """
    def get(self):
        """ Define the get method """
        self.render('login-form.html')

    def post(self):
        """ Define the post method """
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'That username and password combo is invalid'
            self.render('login-form.html', error=msg)
