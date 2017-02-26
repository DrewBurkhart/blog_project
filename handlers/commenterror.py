""" Comment Error class """
from handlers import BaseHandler


class CommentError(BaseHandler):
    """ Create Comment Error class """
    def get(self):
        """ Define the get method for this class """
        self.write("Something happened. I'm as lost as you are...")
