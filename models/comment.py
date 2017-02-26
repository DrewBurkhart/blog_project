""" Comment class """
from google.appengine.ext import db


class Comment(db.Model): #pylint: disable=R0903
    """ Class for comments """
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
