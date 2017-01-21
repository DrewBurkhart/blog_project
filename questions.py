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






ERROR    2017-01-21 20:24:42,375 wsgi.py:279]
Traceback (most recent call last):
  File "/google-cloud-sdk/platform/google_appengine/google/appengine/runtime/wsgi.py", line 267, in Handle
    result = handler(dict(self._environ), self._StartResponse)
  File "/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.3/webapp2.py", line 1519, in __call__
    response = self._internal_error(e)
  File "/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.3/webapp2.py", line 1511, in __call__
    rv = self.handle_exception(request, response, e)
  File "/Developer/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.3/webapp2.py", line 1505, in __call__
    rv = self.router.dispatch(request, response)
  File "/Developer/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.3/webapp2.py", line 1253, in default_dispatcher
    return route.handler_adapter(request, response)
  File "/google-cloud-sdk/platform/google_appengine/lib/webapp2-2.3/webapp2.py", line 1040, in __call__
    return self.handler(request, *args, **kwargs)
  File "/Udacity/blogproject/decorators/post_exists.py", line 22, in wrapper
    self.error(404)
  File "/google-cloud-sdk/platform/google_appengine/lib/webob-1.1.1/webob/request.py", line 1238, in __getattr__
    raise AttributeError(attr)
AttributeError: error
INFO     2017-01-21 20:24:42,380 module.py:806] default: "GET /blog/6605041225957376/deletepost HTTP/1.1" 500 -


class AdhocAttrMixin(object):
    _setattr_stacklevel = 3

    def __setattr__(self, attr, value, DEFAULT=object()):
        if (getattr(self.__class__, attr, DEFAULT) is not DEFAULT or
                    attr.startswith('_')):
            object.__setattr__(self, attr, value)
        else:
            self.environ.setdefault('webob.adhoc_attrs', {})[attr] = value

    def __getattr__(self, attr, DEFAULT=object()):
        try:
            return self.environ['webob.adhoc_attrs'][attr]
        except KeyError:
            raise AttributeError(attr)
