import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from models import *
from handlers import *
from string import letters
from google.appengine.ext import db


def post_exists(function):
    def wrapper(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if post:
            return function(self, post_id, post)
        else:
            self.error(404)
            return
    return wrapper
