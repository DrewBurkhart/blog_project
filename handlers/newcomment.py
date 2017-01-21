import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from handlers import BaseHandler
from string import letters
from google.appengine.ext import db


class NewComment(BaseHandler):
    def get(self, post_id):
        if not self.user:
            return self.redirect("/login")
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
