""" Error Handler """
from handlers import BaseHandler


class Error(BaseHandler):
    def get(self):
        self.render('error.html')
