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
def blog_key(name='default'):
   return db.Key.from_path('blogs', name)


def user_owns_post(function):
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        author = post.author
        loggedUser = self.user.name

        if author == loggedUser:
            if function == EditPost:
                return function(self, post_id)
            elif function == DeletePost:
                return function(self, post_id)
            elif function == DislikePost:
                error = "How about we just delete this one?"
                self.render('error.html', error = error)
            elif function == LikePost:
                error = "You can only like posts that you did not create"
                self.render("error.html", error = error)

        else:
            if function == EditPost:
                error = "You can only edit your own posts"
                self.render("front.html", error = error)
            elif function == DeletePost:
                error = "You can only delete your own posts"
                self.render("front.html", error = error)
            elif function == DislikePost:
                return function(self, post_id)
            elif function == LikePost:
                return function(self, post_id)

    return wrapper
