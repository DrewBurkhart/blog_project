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

def comment_exists(function):
    """ Validate if the comment exists """
    def wrapper(self, *args):
        """ Define wrapper """
        key = db.Key.from_path('Post', int(args[0]), parent=blog_key())
        post = db.get(key)
        comment_key = db.Key.from_path('Comment', int(args[1]),
                                       parent=post.key())
        comment = db.get(comment_key)
        # print comment

        if comment is None:
            self.redirect('/')

        else:
            return function(self, *args)
    return wrapper
