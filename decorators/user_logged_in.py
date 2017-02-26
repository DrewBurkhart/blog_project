""" decorator """
import os
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def user_logged_in(function):
    """ Validate that the user is logged in """
    def wrapper(self, *args):
        """ Define the wrapper """
        if self.user:
            return function(self, *args)

        else:
            self.redirect("/login")
    return wrapper
