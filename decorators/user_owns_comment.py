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
<<<<<<< HEAD

=======
>>>>>>> 975d6cc92a91030bbba4599d9b2f66caaaa3392a

# Duplicate of comment class due to circular reference

class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

# End of duplication

def blog_key(name='default'):
   return db.Key.from_path('blogs', name)

def user_owns_comment(function):
<<<<<<< HEAD
    def wrapper(self, *args):
        key = db.Key.from_path('Post', int(args[0]), parent=blog_key())
        post = db.get(key)
        comment_key = db.Key.from_path('Comment', int(args[1]),
                                parent=self.user.key())
        comment = db.get(comment_key)
        print post
        print comment
        print self.user.key()
=======
    def wrapper(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comment_key = db.Key.from_path('Comment', int(comment_id),
                               parent=self.user.key())
        comment = db.get(comment_key)
        #comment = Comment.get_by_id(int(comment_id), parent=self.user.key())
>>>>>>> 975d6cc92a91030bbba4599d9b2f66caaaa3392a
        author = comment.author
        loggedUser = self.user.name

        if author == loggedUser:
            return function(self, *args)

        else:
            error = "You can only edit your own comments"
            self.render("front.html", error = error)
    return wrapper
