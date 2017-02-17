import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from models import *
from handlers import *
from string import letters
from functools import wraps
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

def comment_exists(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        print args
        # key = db.Key.from_path('Post', int(args[1]), parent=blog_key())
        # post = db.get(key)
        # comment_key = db.Key.from_path('Comment', int(args[2]),
        #                         parent=self.user.key())
        # comment = db.get(comment_key)
        #
        # if comment is None:
        #     self.redirect('/')
        #
        # else:
        return function(self, *args, **kwargs)
    return wrapper
