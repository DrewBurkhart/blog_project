import os
import re
import random
import hashlib
import hmac
import time
import webapp2
# import jinja2
# from handlers import BaseHandler
from string import letters
from google.appengine.ext import db


class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
