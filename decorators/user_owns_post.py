""" decorator """
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)
def blog_key(name='default'):
    """ Define the blog key """
    return db.Key.from_path('blogs', name)

def user_owns_post(function):
    """ Validate that the user owns the post """
    def wrapper(self, *args):
        """ Define the wrapper """
        if not self.user:
            self.redirect("/login")

        else:
            key = db.Key.from_path('Post', int(args[0]), parent=blog_key())
            post = db.get(key)
            author = post.author
            loggedUser = self.user.name

            if author == loggedUser:
                return function(self, *args)
            else:
                error = "You can only edit your own posts"
                self.render("front.html", error=error)
    return wrapper
