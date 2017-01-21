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



class DislikePost(BaseHandler):
    def get(self, post_id):

        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if post is None:
                error = "Something happened. I'm as lost as you are..."
                self.render("error.html", error = error)
            elif post.author == self.user.name:
                error = "How about we just delete this one?"
                self.render('error.html', error = error)
            elif self.user.name in post.disliked_by:
                error = "Ok Ok, you REALLY dislike this post but once is good"
                self.render("error.html", error = error)

            elif self.user.name in post.liked_by:
                post.likes -= 1
                post.liked_by.remove(self.user.name)
                post.dislikes += 1
                post.disliked_by.append(self.user.name)
                post.put()

                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                " created ASC limit 10")

                self.render('front.html', posts=posts, comments=comments)

            else:
                post.dislikes += 1
                post.disliked_by.append(self.user.name)
                post.put()

                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                " created ASC limit 10")

                self.render('front.html', posts=posts, comments=comments)
