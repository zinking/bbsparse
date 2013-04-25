from django.conf import settings
from django.http import *
from django.template.loader import render_to_string as rts;

class GbkHttpResponse(HttpResponse):
    """
    return gbk encoding response
    """
    status_code = 200
    def __init__(self, content='', mimetype=None, status=None, content_type=None):
        self._charset = 'gbk'
        content_type = "text/html; charset=gbk"
        if not isinstance(content, basestring) and hasattr(content, '__iter__'):
            self._container = content
            self._is_string = False
        else:
            self._container = [content]
            self._is_string = True
        self.cookies = SimpleCookie()
        self._headers = {'content-type': ('Content-Type', content_type)}

def render_to_response(*args, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    django.template.loader.render_to_string() with the passed arguments.
    """
    httpresponse_kwargs = {'mimetype': kwargs.pop('mimetype', None)}
    try:
        response = GbkHttpResponse(rts(*args, **kwargs), **httpresponse_kwargs);
    except Exception,e:
        #maybe there's some UTF responses
        try:
            response = HttpResponse(rts(*args, **kwargs), **httpresponse_kwargs);
        except Exception,e:
            #other exceptions, raise
            raise e;
        return response;
    return response;
