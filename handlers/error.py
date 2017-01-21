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

class Error(BaseHandler):
    def get(self):
        self.render('error.html')
