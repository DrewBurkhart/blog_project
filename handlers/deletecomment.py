""" Delete Comment Handler """
from handlers import BaseHandler
from google.appengine.ext import db


def blog_key(name='default'):
    """ Define the blog key """
    return db.Key.from_path('blogs', name)

class Comment(db.Model): #pylint: disable=R0903
    """ Duplicate Comment class due to circular reference """
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

class DeleteComment(BaseHandler):
    """ Handler to Delete a comment """
    @comment_exists #pylint: disable=E0602
    @user_owns_comment #pylint: disable=E0602
    def get(self, post_id, comment_id):
        """ Define the get method """
        if self.user:
            comment = Comment.get_by_id(int(comment_id),
                                        parent=self.user.key())
            # key = db.Key.from_path('Post', int(post_id), parent=blog_key())

            if comment:
                comment.delete()
                self.redirect('/blog')
            else:
                self.redirect('/commenterror')
        else:
            self.redirect("/login")
