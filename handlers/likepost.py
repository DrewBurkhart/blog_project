""" Like Post Handler """
from handlers import BaseHandler
from google.appengine.ext import db
from decorators import post_exists, user_not_own_post


def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class LikePost(BaseHandler):
    @post_exists
    @user_not_own_post
    def get(self, post_id):
            # checks user
        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if post is None:
                error = "Something happened. I'm as lost as you are..."
                self.render("error.html", error=error)
                return
            logged_user = self.user.name

            if logged_user in post.liked_by:
                error = "We get it, you REALLY like this post but once is good"
                self.render("error.html", error=error)

            elif logged_user in post.disliked_by:
                # post.dislikes -= 1
                post.disliked_by.remove(logged_user)
                # post.likes += 1
                post.liked_by.append(logged_user)
                post.put()

                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                    " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                       " created ASC limit 10")

                self.render('front.html', posts=posts, comments=comments)

            else:
                # post.likes += 1
                post.liked_by.append(logged_user)
                post.put()
                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                    " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                       " created ASC limit 10")
                self.render('front.html', posts=posts, comments=comments)
