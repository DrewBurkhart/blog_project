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

# Duplicate Post and Comment class due to circular reference

class Post(db.Model):
    subject = db.StringProperty(required=True, multiline=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(required=True)
    dislikes = db.IntegerProperty(required=True)
    liked_by = db.ListProperty(str)
    disliked_by = db.ListProperty(str)

    def render(self):
    	self._render_text = self.content.replace('\n', '<br>')
    	return render_str("post.html", p = self)

class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

# End of duplication

class NewComment(BaseHandler):
    @user_logged_in
    def get(self, post_id):
        post = Post.get_by_id(int(post_id), parent=blog_key())

        if post is None:
            self.redirect('/')

        else:
            subject = post.subject
            content = post.content
            self.render("comment.html",
                        subject=subject,
                        content=content,
                        comment="")

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            return self.error(404)
        if not self.user:
            return self.redirect("/login")

        comment = self.request.get("comment")

        if comment:
            author = self.user.name
            c = Comment(comment= comment, post= post_id,
                        author= author, parent= self.user.key())
            c.put()
            self.redirect('/blog')

        else:
            error = "I thought you wanted to comment?"
            self.render("comment.html",
                        post = post,
                        error = error)
