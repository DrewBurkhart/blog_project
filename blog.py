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

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class MainPage(BaseHandler):
    def get(self):
        self.redirect("/blog")


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class FrontPage(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created ASC limit 10") #NOQA

        self.render('front.html', posts = posts, comments = comments)

    def post(self):
        newpost = self.request.get("newPost")

        if newpost:
            self.redirect("/blog/newpost")


class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            return self.error(404)
        self.render("permalink.html", post = post)



app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', FrontPage),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/blog/([0-9]+)/editpost', EditPost),
                               ('/blog/([0-9]+)/like', LikePost),
                               ('/blog/([0-9]+)/dislike', DislikePost),
                               ('/login', Login),
                               ('/error', Error),
                               ('/logout', Logout),
                               ('/blog/([0-9]+)/comment', NewComment),
                               ('/blog/([0-9]+)/editcomment/([0-9]+)',
                                EditComment),
                               ('/blog/([0-9]+)/deletecomment/([0-9]+)',
                                DeleteComment),
                               ('/commenterror', CommentError),
                               ('/blog/([0-9]+)/deletepost', DeletePost)
                               ],
                               debug=True)
