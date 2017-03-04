""" New Post class """
import os
import jinja2
from handlers import BaseHandler
from google.appengine.ext import db
from models import Post
from decorators import user_not_logged_in

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class NewPost(BaseHandler):
    @user_not_logged_in
    def get(self):
        self.render("newpost.html")

    @user_not_logged_in
    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')
        author = self.user.name

        if subject and content:
            p = Post(parent=blog_key(), subject=subject,
                     content=content, author=author, likes=0,
                     dislikes=0, disliked_by=[], liked_by=[])
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))

        else:
            error = "Please enter both subject and some content"
            self.render(
                "newpost.html", subject=subject, content=content, error=error)
