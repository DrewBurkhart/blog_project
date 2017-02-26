""" Post class """
import os
import jinja2
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    """ Define the render string function """
    t = jinja_env.get_template(template)
    return t.render(params)

class Post(db.Model): #pylint: disable=R0903
    """ Create the post class """
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
        """ Define the render function """
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)
