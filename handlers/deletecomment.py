""" Delete Comment Handler """
from handlers import BaseHandler
from google.appengine.ext import db
from decorators import comment_exists, user_owns_comment


def blog_key(name='default'):
    """ Define the blog key """
    return db.Key.from_path('blogs', name)


class Comment(db.Model):
    """ Duplicate Comment class due to circular reference """
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class DeleteComment(BaseHandler):
    """ Handler to Delete a comment """
    @comment_exists
    @user_owns_comment
    def get(self, post_id, comment_id):
        """ Define the get method """
        if self.user:
            comment = Comment.get_by_id(int(comment_id),
                                        parent=self.user.key())

            if comment:
                comment.delete()
                self.redirect('/blog')
            else:
                self.redirect('/commenterror')
        else:
            self.redirect("/login")
