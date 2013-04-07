"""This is some simple helper code to bridge the Pylons / pyXn gap.

There's some generic WSGI middleware, some Paste stuff, and some Pylons
stuff.  Once you put XiaoneiWSGIMiddleware into your middleware stack,
you'll have access to ``environ["pyxn.xiaonei"]``, which is a
``pyxn.Xiaonei`` object.  If you're using Paste (which includes
Pylons users), you can also access this directly using the xiaonei
global in this module.

"""

# Be careful what you import.  Don't expect everyone to have Pylons,
# Paste, etc. installed.  Degrade gracefully.

from pyxn import Xiaonei

__docformat__ = "restructuredtext"


# Setup Paste, if available.  This needs to stay in the same module as
# XiaoneiWSGIMiddleware below.

try:
    from paste.registry import StackedObjectProxy
    from paste.httpexceptions import _HTTPMove
except ImportError:
    pass
else:
    xiaonei = StackedObjectProxy(name="pyXn Xiaonei Connection")


    class CanvasRedirect(_HTTPMove):

        """This is for canvas redirects."""

        title = "See Other"
        code = 200
        template = '<xn:redirect url="%(location)s" />'


class XiaoneiWSGIMiddleware(object):

    """This is WSGI middleware for Xiaonei."""

    def __init__(self, app, config, xiaonei_class=Xiaonei):
        """Initialize the Xiaonei middleware.

        ``app``
            This is the WSGI application being wrapped.

        ``config``
            This is a dict containing the keys "pyfacebook.apikey" and
            "pyfacebook.secret".

        ``xiaonei_class``
            If you want to subclass the Xiaonei class, you can pass in
            your replacement here.  Pylons users will want to use
            PylonsXiaonei.

        """
        self.app = app
        self.config = config
        self.facebook_class = xiaonei_class

    def __call__(self, environ, start_response):
        config = self.config
        real_facebook = self.facebook_class(config["pyxn.apikey"],
                                            config["pyxn.secret"])
        registry = environ.get('paste.registry')
        if registry:
            registry.register(xiaonei, real_facebook)
        environ['pyxn.xiaonei'] = real_facebook
        return self.app(environ, start_response)


# The remainder is Pylons specific.

try:
    import pylons
    from pylons.controllers.util import redirect_to as pylons_redirect_to
    from webhelpers import url_for
except ImportError:
    pass
else:


    class PylonsXiaonei(Xiaonei):

        """Subclass Xiaonei to add Pylons goodies."""

        def check_session(self, request=None):
            """The request parameter is now optional."""
            if request is None:
                request = pylons.request
            return Xiaonei.check_session(self, request)

        # The Django request object is similar enough to the Paste
        # request object that check_session and validate_signature
        # should *just work*.

        def redirect_to(self, url):
            """Wrap Pylons' redirect_to function so that it works not in_iframe.

            By the way, this won't work until after you call
            check_session().

            """
            if not self.in_iframe:
                raise CanvasRedirect(url)
            pylons_redirect_to(url)

        def apps_url_for(self, *args, **kargs):
            """Like url_for, but starts with "http://apps.xiaonei.com"."""
            return "http://apps.xiaonei.com" + url_for(*args, **kargs)


    def create_pylons_xiaonei_middleware(app, config):
        """This is a simple wrapper for XiaoneiWSGIMiddleware.

        It passes the correct facebook_class.

        """
        return XiaoneiWSGIMiddleware(app, config,
                                      xiaonei_class=PylonsXiaonei)
