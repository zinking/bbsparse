import logging
import pyxn

from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

__all__ = ['Xiaonei', 'XiaoneiMiddleware', 'get_xiaonei_client', 'require_login', 'require_add']

_thread_locals = local()

class Xiaonei(pyxn.Xiaonei):
    def redirect(self, url):
        """
        Helper for Django which redirects to another page. If inside a
        canvas page, writes a <xn:redirect> instead to achieve the same effect.

        """
        #return HttpResponse('<xn:redirect url="%s" />' % (url, )) NOT USED WHEN USING IFRAME
        #logging.debug('It is redirected here 2 %s'%(url));
        return HttpResponseRedirect(url);

def get_xiaonei_client():
    """
    Get the current Xiaonei object for the calling thread.

    """
    try:
        return _thread_locals.xiaonei
    except AttributeError:
        raise ImproperlyConfigured('Make sure you have the Xiaonei middleware installed.')


def require_login(next=None, internal=None):
    """
    Decorator for Django views that requires the user to be logged in.
    The XiaoneiMiddleware must be installed.

    Standard usage:
        @require_login()
        def some_view(request):
            ...

    Redirecting after login:
        To use the 'next' parameter to redirect to a specific page after login, a callable should
        return a path relative to the Post-add URL. 'next' can also be an integer specifying how many
        parts of request.path to strip to find the relative URL of the canvas page. If 'next' is None,
        settings.callback_path and settings.app_name are checked to redirect to the same page after logging
        in. (This is the default behavior.)
        @require_login(next=some_callable)
        def some_view(request):
            ...
    """
    def decorator(view):
        def newview(request, *args, **kwargs):
            next = newview.next
            internal = newview.internal

            try:
                xn = request.xiaonei
            except:
                raise ImproperlyConfigured('Make sure you have the Xiaonei middleware installed.')

            if internal is None:
                internal = request.xiaonei.internal

            if callable(next):
                next = next(request.path)
            elif isinstance(next, int):
                next = '/'.join(request.path.split('/')[next + 1:])
            elif next is None and xn.callback_path and request.path.startswith(xn.callback_path):
                next = request.path[len(xn.callback_path):]
            elif not isinstance(next, str):
                next = ''

            if not xn.check_session(request):
                #If user has never logged in before, the get_login_url will redirect to the TOS page
#                logging.debug('user never logged in, redirect to login url')
                return xn.redirect(xn.get_login_url(next=next))

            if internal and request.method == 'GET' and xn.app_name:
                return xn.redirect('%s%s' % (xn.get_app_url(), next))

            return view(request, *args, **kwargs)
        newview.next = next
        newview.internal = internal
        return newview
    return decorator


def require_add(next=None, internal=None, on_install=None):
    """
    Decorator for Django views that requires application installation.
    The XiaoneiMiddleware must be installed.
    
    Standard usage:
        @require_add()
        def some_view(request):
            ...

    Redirecting after installation:
        To use the 'next' parameter to redirect to a specific page after login, a callable should
        return a path relative to the Post-add URL. 'next' can also be an integer specifying how many
        parts of request.path to strip to find the relative URL of the canvas page. If 'next' is None,
        settings.callback_path and settings.app_name are checked to redirect to the same page after logging
        in. (This is the default behavior.)
        @require_add(next=some_callable)
        def some_view(request):
            ...

    Post-install processing:
        Set the on_install parameter to a callable in order to handle special post-install processing.
        The callable should take a request object as the parameter.
        @require_add(on_install=some_callable)
        def some_view(request):
            ...
    """
    def decorator(view):
        def newview(request, *args, **kwargs):
            next = newview.next
            internal = newview.internal
            logging.debug('new_view ----- >%s'%(next));
            
            try:
                xn = request.xiaonei
            except:
                raise ImproperlyConfigured('Make sure you have the Xiaonei middleware installed.')

            if internal is None:
                internal = request.xiaonei.internal

            if callable(next):
                next = next(request.path)
            elif isinstance(next, int):
                next = '/'.join(request.path.split('/')[next + 1:])
            elif next is None and xn.callback_path and request.path.startswith(xn.callback_path):
                next = request.path[len(xn.callback_path):]
            else:
                next = ''

            
            if not xn.check_session(request):
                if xn.added:
                    if request.method == 'GET' and xn.app_name:
                        return xn.redirect('%s%s' % (xn.get_app_url(), next))
                    return xn.redirect(xn.get_login_url(next=next))
                else:
                    return xn.redirect(xn.get_add_url(next=next))

            if not xn.added:
                return xn.redirect(xn.get_add_url(next=next))

            if 'installed' in request.GET and callable(on_install):
                on_install(request)
            
            if internal and request.method == 'GET' and xn.app_name:
                return xn.redirect('%s%s' % (xn.get_app_url(), next))

            return view(request, *args, **kwargs)
        newview.next = next
        newview.internal = internal
        return newview
    return decorator

# try to preserve the argspecs
try:
    import decorator
except ImportError:
    pass
else:
    def updater(f):
        def updated(*args, **kwargs):
            original = f(*args, **kwargs)
            def newdecorator(view):
                return decorator.new_wrapper(original(view), view)
            return decorator.new_wrapper(newdecorator, original)
        return decorator.new_wrapper(updated, f)
    require_login = updater(require_login)
    require_add = updater(require_add)

class XiaoneiMiddleware(object):
    """
    Middleware that attaches a Xiaonei object to every incoming request.
    The Xiaonei object created can also be accessed from models for the
    current thread by using get_xiaonei_client().

    """

    def __init__(self, api_key=None, secret_key=None, app_name=None, callback_path=None, internal=None):
        self.api_key = api_key or settings.XIAONEI_API_KEY
        self.secret_key = secret_key or settings.XIAONEI_SECRET_KEY
        self.app_name = app_name or getattr(settings, 'XIAONEI_APP_NAME', None)
        self.callback_path = callback_path or getattr(settings, 'XIAONEI_CALLBACK_PATH', None)
        self.internal = internal or getattr(settings, 'XIAONEI_INTERNAL', True)
        self.proxy = None
        if getattr(settings, 'USE_HTTP_PROXY', False):
            self.proxy = settings.HTTP_PROXY

    def process_request(self, request):
        
        request.xiaonei = Xiaonei(self.api_key, self.secret_key, app_name=self.app_name, callback_path=self.callback_path, internal=self.internal, proxy=self.proxy)
        _thread_locals.xiaonei = request.xiaonei;
        #logging.debug( request.xiaonei );
        if not self.internal and 'xiaonei_session_key' in request.session and 'xiaonei_user_id' in request.session:
            #logging.debug('Inject XiaoNei Stuff !!! process_request: %s, ' % request.session)
            request.xiaonei.session_key = request.session['xiaonei_session_key']
            request.xiaonei.uid = request.session['xiaonei_user_id']

    def process_response(self, request, response):
        if not self.internal and request.xiaonei.session_key and request.xiaonei.uid:
            request.session['xiaonei_session_key'] = request.xiaonei.session_key
            request.session['xiaonei_user_id'] = request.xiaonei.uid
        return response
