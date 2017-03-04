""" Delete Post Handler """
from handlers import BaseHandler
from google.appengine.ext import db
from decorators import post_exists, user_owns_post


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class DeletePost(BaseHandler):
    """ Class to delete post """
    @post_exists
    @user_owns_post
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if post is None:
                self.redirect('/')

            else:
                post.delete()
                error = "Post has been deleted"
                self.render("front.html", error=error)

        else:
            self.redirect('/login')
