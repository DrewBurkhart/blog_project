import os
import jinja2
from handlers import BaseHandler
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)



# Duplicated 'Post' class due to circular reference

class Post(db.Model):
    subject = db.StringProperty(required=True, multiline=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    author = db.StringProperty(required=True)
    likes = db.IntegerProperty(required=True)
    dislikes = db.IntegerProperty(required=True)
    liked_by = db.ListProperty(str)
    disliked_by = db.ListProperty(str)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)

# End of duplication


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class NewPost(BaseHandler):
    @user_not_logged_in
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

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
