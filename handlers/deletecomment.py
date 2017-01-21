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



class DeleteComment(BaseHandler):
    def get(self, post_id, comment_id):
        if self.user:
            comment = Comment.get_by_id(int(comment_id),
                                        parent=self.user.key())
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if comment is None:
                error = "You can only delete your own comments"
                self.render("front.html", error = error)
                return

            author = comment.author
            loggedUser = self.user.name

            if author != loggedUser:
                error = "You can only delete your own comments"
                self.render("front.html", error = error)

            elif comment:
                comment.delete()
                self.redirect('/blog')
            else:
                self.redirect('/commenterror')
        else:
            self.redirect("/login")
