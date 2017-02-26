""" decorator """
import os
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

# Duplicate of comment class due to circular reference

class Comment(db.Model): #pylint: disable=R0903
    """ Define the comment class """
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

# End of duplication

def blog_key(name='default'):
    """ Define the blog key """
    return db.Key.from_path('blogs', name)

def user_owns_comment(function):
    """ Validate that the user owns the comment """
    def wrapper(self, *args):
        """ Define the wrapper """
        key = db.Key.from_path('Post', int(args[0]), parent=blog_key())
        post = db.get(key)
        comment_key = db.Key.from_path('Comment', int(args[1]),
                                       parent=self.user.key())
        comment = db.get(comment_key)
        print post
        print comment
        print self.user.key()
        author = comment.author
        loggedUser = self.user.name

        if author == loggedUser:
            return function(self, *args)

        else:
            error = "You can only edit your own comments"
            self.render("front.html", error=error)
    return wrapper
