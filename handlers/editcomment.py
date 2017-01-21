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



class EditComment(BaseHandler):
    def get(self, post_id, comment_id):
        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            comment_key = db.Key.from_path('Comment', int(comment_id),
                                    parent=self.user.key())
            comment = db.get(comment_key)

            if comment is None:
                self.redirect('/')

            else:
                author = comment.author
                loggedUser = self.user.name

                if author != loggedUser:
                    error = "You can only edit your own comments"
                    self.render("front.html", error = error)
                    return

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
