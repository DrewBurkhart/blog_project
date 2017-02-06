import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from handlers import BaseHandler
from decorators import *
from string import letters
from google.appengine.ext import db


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

# Duplicate Comment class due to circular reference

class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

# End of duplication

class DeleteComment(BaseHandler):
    @comment_exists
    @user_owns_comment
    def get(self, post_id, comment_id):
        if self.user:
            comment = Comment.get_by_id(int(comment_id),
                                        parent=self.user.key())
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())

            if comment:
                comment.delete()
                self.redirect('/blog')
            else:
                self.redirect('/commenterror')
        else:
            self.redirect("/login")
