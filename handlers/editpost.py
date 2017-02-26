""" Edit Post Handler """
from handlers import BaseHandler
from google.appengine.ext import db



def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class EditPost(BaseHandler):
    @user_owns_post
    @post_exists
    def get(self, post_id):

        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            error = ""
            self.render("editpost.html", subject = post.subject,
                        content = post.content, error = error)


    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id),
                                parent=blog_key())

        if not self.user:
            self.redirect("/login")

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            p = db.get(key)
            p.subject = self.request.get('subject')
            p.content = self.request.get('content')
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
