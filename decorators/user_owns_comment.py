import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
import models
from handlers import *
from string import letters
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
def blog_key(name='default'):
   return db.Key.from_path('blogs', name)

class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

def user_owns_comment(function):
    def wrapper(self, post_id, comment_id):
        comment = Comment.get_by_id(int(comment_id), parent= self.user.key())
        # author = comment.author
        loggedUser = self.user.name

        if comment.author != loggedUser:
            error = "You can only edit your own comments"
            self.render("front.html", error = error)
            return

        else:
            return function(self, post_id, comment_id)
    return wrapper
