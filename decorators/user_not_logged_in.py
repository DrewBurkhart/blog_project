""" decorator """
import os
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def user_not_logged_in(function):
    """ Check if the user is not logged in """
    def wrapper(self):
        """ Define the wrapper """
        if self.user:
            return function(self)

        else:
            self.redirect("/login")
    return wrapper
