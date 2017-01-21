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
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def user_owns_post(function):
    def wrapper(self, post_id):
        author = post.author
        loggedUser = self.user.name
        if author == loggedUser:
            return function(self, post_id, post)
        else:
            error = "You can only edit your own posts"
            self.render("front.html", error = error)
    return wrapper
