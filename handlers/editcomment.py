""" Edit Comment Handler """
from handlers import BaseHandler
from google.appengine.ext import db
from models import Comment
from decorators import user_owns_comment, comment_exists, user_not_logged_in


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class EditComment(BaseHandler):
    @user_owns_comment
    @comment_exists
    def get(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comment = Comment.get_by_id(int(comment_id), parent=post.key())

        if not self.user:
            self.redirect('/login')

        else:
            error = ""
            self.render("comment.html", comment=comment.comment)

    def post(self, post_id, comment_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())

        if not self.user:
            self.redirect("/login")

        else:
            post = db.get(key)
            comment = Comment.get_by_id(int(comment_id), parent=post.key())
            c = Comment.get_by_id(int(comment_id), parent=post.key())
            c.comment = self.request.get('comment')

            if c.comment:
                c.put()
                self.redirect('/blog')

            else:
                error = "You know there was a 'Delete' button right?"
                self.render('comment.html', error=error, comment=c.comment)
