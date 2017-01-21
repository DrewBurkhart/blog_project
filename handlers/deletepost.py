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


class DeletePost(BaseHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            author = post.author
            loggedUser = self.user.name

            if post is None:
                self.redirect('/')

            elif author != loggedUser:
                error = "You can only delete your own posts"
                self.render("front.html", error = error)

            else:
                post.delete()
                error = "Post has been deleted"
                self.render("front.html", error = error)

        else:
            self.redirect('/login')
