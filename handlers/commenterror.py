import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from handlers import BaseHandler
from string import letters
from google.appengine.ext import db


class CommentError(BaseHandler):
    def get(self):
        self.write("Something happened. I'm as lost as you are...")
