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


# Duplicate of comment class due to circular reference

class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

# End of duplication



class EditComment(BaseHandler):
    @comment_exists
    @user_owns_comment
    def get(self, post_id, comment_id):
        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent= blog_key())
            post = db.get(key)
            error = ""
            self.render("comment.html", comment = comment.comment)

    def post(self, post_id, comment_id):
        comment = Comment.get_by_id(int(comment_id), parent= self.user.key())
        com = self.request.get("comment")

        if com:
            if comment.parent().key().id() == self.user.key().id():
                com = comment.comment
                comment.put()
            self.redirect('/blog')

        else:
            error = "You know there was a 'Delete' button right?"
            self.render('comment.html', error = error)
