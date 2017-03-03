""" decorator """
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def blog_key(name='default'):
    """ Define Blog Key """
    return db.Key.from_path('blogs', name)


def post_exists(function):
    """ Validate that the post exists """
    def wrapper(self, *args):
        """ Define the wrapper """
        key = db.Key.from_path('Post', int(args[0]), parent=blog_key())
        post = db.get(key)

        if post:
            return function(self, *args)

        else:
            error = "This post does not exist"
            # print self
            self.render("front.html", error=error)
    return wrapper
