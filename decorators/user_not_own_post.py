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

def user_not_own_post(function):
    """ Check to see if the user does not own the post """
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
                error = "You can't like your own posts"
                self.render("front.html", error=error)
            else:
                return function(self, *args)

    return wrapper
