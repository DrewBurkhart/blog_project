import os
import re
import random
import hashlib
import hmac
import time
import webapp2
import jinja2
from string import letters
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)



def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


# Functions for hashing and passwords
secret = 'ie7dj^uejd(92due63ye^&uejd7364@'

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


# Main BaseHandler class that other classes will inherit from
class BaseHandler(webapp2.RequestHandler):
    # Makes it so you don't have to write response.out. every time
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))



class MainPage(BaseHandler):
    def get(self):
        self.redirect("/blog")



# used for hashing password by making a salt and applying it to pw
def make_salt(length=5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group='default'):
    return db.Key.from_path('users', group)



#########USER#########

# Defines User class and creates methods
# to retrieve users and their info
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = cls.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return cls(parent = users_key(),
                   name = name,
                   pw_hash = pw_hash,
                   email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u



#########BLOG#########

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


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
    	return render_str("post.html", p = self)


class Comment(db.Model):
    comment = db.TextProperty()
    post = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class NewPost(BaseHandler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            self.redirect("/login")

    def post(self):
        if not self.user:
            return self.redirect('/login')

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
                "newpost.html", subject= subject, content= content, error= error)


class NewComment(BaseHandler):
    def get(self, post_id):
        if not self.user:
            return self.redirect("/login")
        post = Post.get_by_id(int(post_id), parent=blog_key())

        if post is None:
            self.redirect('/')

        else:
            subject = post.subject
            content = post.content
            self.render("comment.html",
                        subject=subject,
                        content=content,
                        comment="")

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            return self.error(404)
        if not self.user:
            return self.redirect("/login")

        comment = self.request.get("comment")

        if comment:
            author = self.user.name
            c = Comment(comment= comment, post= post_id,
                        author= author, parent= self.user.key())
            c.put()
            self.redirect('/blog')

        else:
            error = "I thought you wanted to comment?"
            self.render("comment.html",
                        post = post,
                        error = error)


class EditComment(BaseHandler):
    def get(self, post_id, comment_id):
        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            comment_key = db.Key.from_path('Comment', int(comment_id),
                                    parent=self.user.key())
            comment = db.get(comment_key)

            if comment is None:
                self.redirect('/')

            else:
                author = comment.author
                loggedUser = self.user.name

                if author != loggedUser:
                    error = "You can only edit your own comments"
                    self.render("front.html", error = error)
                    return

                else:
                    key = db.Key.from_path('Post', int(post_id), parent= blog_key())
                    post = db.get(key)
                    error = ""
                    self.render("comment.html", comment = comment.comment)

    def post(self, post_id, comment_id):
        comment = Comment.get_by_id(int(comment_id), parent= self.user.key())
        com = self.request.get("comment")

        if com:
            if comment.parent().key().id() == self.user.key().id():
                com = comment.comment
                comment.put()
            self.redirect('/blog')

        else:
            error = "You know there was a 'Delete' button right?"
            self.render('comment.html', error = error)


class DeleteComment(BaseHandler):
    def get(self, post_id, comment_id):
        if self.user:
            comment = Comment.get_by_id(int(comment_id),
                                        parent=self.user.key())
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if comment is None:
                error = "You can only delete your own comments"
                self.render("front.html", error = error)
                return

            author = comment.author
            loggedUser = self.user.name

            if author != loggedUser:
                error = "You can only delete your own comments"
                self.render("front.html", error = error)

            elif comment:
                comment.delete()
                self.redirect('/blog')
            else:
                self.redirect('/commenterror')
        else:
            self.redirect("/login")


class DeletePost(BaseHandler):
    def get(self, post_id):
        if self.user:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            author = post.author
            loggedUser = self.user.name

            if post is None:
                self.redirect('/')

            elif author != loggedUser:
                error = "You can only delete your own posts"
                self.render("front.html", error = error)

            else:
                post.delete()
                error = "Post has been deleted"
                self.render("front.html", error = error)

        else:
            self.redirect('/login')


class CommentError(BaseHandler):
    def get(self):
        self.write("Something happened. I'm as lost as you are...")


class FrontPage(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        comments = db.GqlQuery("SELECT * FROM Comment ORDER BY created ASC limit 10") #NOQA

        self.render('front.html', posts = posts, comments = comments)

    def post(self):
        newpost = self.request.get("newPost")

        if newpost:
            self.redirect("/blog/newpost")


class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            return self.error(404)
        self.render("permalink.html", post = post)


class LikePost(BaseHandler):
    def get(self, post_id):\
            # checks user
        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if post is None:
                error = "Something happened. I'm as lost as you are..."
                self.render("error.html", error = error)
                return
            author = post.author
            logged_user = self.user.name

            if author == logged_user:
                error = "You can only like posts that you did not create"
                self.render("error.html", error = error)
            elif logged_user in post.liked_by:
                error = "We get it, you REALLY like this post but once is good"
                self.render("error.html", error = error)

            elif logged_user in post.disliked_by:
                post.dislikes -= 1
                post.disliked_by.remove(logged_user)
                post.likes += 1
                post.liked_by.append(logged_user)
                post.put()

                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                " created ASC limit 10")

                self.render('front.html', posts=posts, comments=comments)

            else:
                post.likes += 1
                post.liked_by.append(logged_user)
                post.put()
                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                " created ASC limit 10")
                self.render('front.html', posts=posts, comments=comments)


class DislikePost(BaseHandler):
    def get(self, post_id):

        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if post is None:
                error = "Something happened. I'm as lost as you are..."
                self.render("error.html", error = error)
            elif post.author == self.user.name:
                error = "How about we just delete this one?"
                self.render('error.html', error = error)
            elif self.user.name in post.disliked_by:
                error = "Ok Ok, you REALLY dislike this post but once is good"
                self.render("error.html", error = error)

            elif self.user.name in post.liked_by:
                post.likes -= 1
                post.liked_by.remove(self.user.name)
                post.dislikes += 1
                post.disliked_by.append(self.user.name)
                post.put()

                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                " created ASC limit 10")

                self.render('front.html', posts=posts, comments=comments)

            else:
                post.dislikes += 1
                post.disliked_by.append(self.user.name)
                post.put()

                posts = db.GqlQuery("SELECT * FROM Post ORDER BY" +
                                " created DESC limit 10")
                comments = db.GqlQuery("SELECT * FROM Comment ORDER BY" +
                                " created ASC limit 10")

                self.render('front.html', posts=posts, comments=comments)


class EditPost(BaseHandler):
    def get(self, post_id):

        if not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)

            if post is None:
                self.redirect('/')

            else:
                author = post.author
                loggedUser = self.user.name

            if author == loggedUser:
                key = db.Key.from_path('Post', int(post_id), parent=blog_key())
                post = db.get(key)
                error = ""
                self.render("editpost.html", subject = post.subject,
                            content = post.content, error = error)
            else:
                error = "You can only edit your own posts"
                self.render("front.html", error = error)

    def post(self, post_id):
        key = db.Key.from_path('Post', int(post_id),
                                parent=blog_key())
        post = db.get(key)
        author = post.author
        loggedUser = self.user.name

        if not self.user:
            self.redirect("/login")

        elif author != loggedUser:
            self.redirect("/login")

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            p = db.get(key)
            p.subject = self.request.get('subject')
            p.content = self.request.get('content')
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))




# Defining the constraints for our username, pw and email addresses
def valid_username(username):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return username and USER_RE.match(username)

def valid_password(password):
    PASS_RE = re.compile(r"^.{3,20}$")
    return password and PASS_RE.match(password)

def valid_email(email):
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
    return not email or EMAIL_RE.match(email)





class Signup(BaseHandler):
    def get(self):
        self.render("signup-form.html")

    def post(self):
        has_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.reenter = self.request.get('reenter')
        self.email = self.request.get('email')

        params = dict(username=self.username,
                      email=self.email)

        if not valid_username(self.username):
            params['error_username'] = "Invalid username"
            has_error = True

        if not valid_password(self.password):
            params['error_password'] = "Invalid password"
            has_error = True

        elif self.password != self.reenter:
            params['error_reenter'] = "Your passwords didn't match."
            has_error = True

        if not valid_email(self.email):
            params['error_email'] = "Invalid email"
            has_error = True

        if has_error:
            self.render('signup-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'Name taken. Someone else beat you to it.'
            self.render('signup-form.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')


class Login(BaseHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'That username and password combo is invalid'
            self.render('login-form.html', error=msg)


class Error(BaseHandler):
    def get(self):
        self.render('error.html')


class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/blog/?', FrontPage),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/blog/([0-9]+)/editpost', EditPost),
                               ('/blog/([0-9]+)/like', LikePost),
                               ('/blog/([0-9]+)/dislike', DislikePost),
                               ('/login', Login),
                               ('/error', Error),
                               ('/logout', Logout),
                               ('/blog/([0-9]+)/', NewComment),
                               ('/blog/([0-9]+)/editcomment/([0-9]+)',
                                EditComment),
                               ('/blog/([0-9]+)/deletecomment/([0-9]+)',
                                DeleteComment),
                               ('/commenterror', CommentError),
                               ('/blog/([0-9]+)/deletepost', DeletePost)
                               ],
                               debug=True)
