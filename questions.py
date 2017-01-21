# DECORATOR DEFINITION

def user_owns_post(function):
    @wraps(function)
    def wrapper(self, post_id):
        author = post.author
        loggedUser = self.user.name
        if author == loggedUser:
            return function(self, post_id, post)
        else:
            error = "You can only edit your own posts"
            self.render("front.html", error = error)
    return wrapper




# HANDLER USING DECORATOR

class EditPost(BaseHandler):
    @post_exists
    @user_owns_post
    def get(self, post_id):

        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            error = ""
            self.render("editpost.html", subject = post.subject,
                        content = post.content, error = error)
