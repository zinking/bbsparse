#! /usr/bin/env python
# pyxn - Python bindings for the Xiaonei API
# Copyright (c) 2008, (Damien) Yongrong Hou houyongr(at)gmail dot com
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This work is based on pyfacebook, whose license is shown below
#
# Copyright (c) 2008, Samuel Cormier-Iijima
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY <copyright holder> ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
Python bindings for the Xiaonei API (pyxn - http://code.google.com/p/pyxn)

pyxn is a client library that wraps the Xiaonei API.

For more information, see

Home Page: http://code.google.com/p/pyxn
Developer Wiki: http://code.google.com/p/pyxn/w/list

Response format defaults to XML, since Xiaonei API currently doesn't return JSON
for some of the API calls
May switch to JSON when Xiaonei supports it
"""

import logging
import md5
import sys
import time
import urllib
import urllib2
import httplib
import urlparse
import mimetypes

try:
    import simplejson
except ImportError:
    try:
        from django.utils import simplejson
    except ImportError:
        pass

from xml.dom import minidom
RESPONSE_FORMAT = 'XML'
# support Google App Engine.  GAE does not have a working urllib.urlopen.
try:
    from google.appengine.api import urlfetch

    def urlread(url, data=None):
        if data is not None:
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            method = urlfetch.POST
        else:
            headers = {}
            method = urlfetch.GET

        result = urlfetch.fetch(url, method=method,
                                payload=data, headers=headers)
        
        if result.status_code == 200:
            return result.content
        else:
            raise urllib2.URLError("fetch error url=%s, code=%d" % (url, result.status_code))

except ImportError:
    def urlread(url, data=None):
        res = urllib2.urlopen(url, data=data)
        return res.read()
    
__all__ = ['Xiaonei']

VERSION = '0.1'

# REST URLs
XIAONEI_URL = 'http://api.xiaonei.com/restserver.do'
XIAONEI_SECURE_URL = 'https://api.xiaonei.com/restserver.do'

class json(object): pass

# simple IDL for the Xiaonei API
METHODS = {
    # feed methods
    'feed': {
        'publishTemplatizedAction': [
            ('template_id', int, []),
            ('title_data', json, ['optional']),
            ('body_data', json, ['optional']),
            ('resource_id', int, ['optional']),
        ],
    },

    # friends methods
    'friends': {
        'areFriends': [
            ('uids1', list, []),
            ('uids2', list, []),
        ],

        'getFriends': [],

        'getAppUsers': [],
        
        'get': [],
    },

    # notifications methods
    'notifications': {
#        'get': [],

        'send': [
            ('to_ids', list, []),
            ('notification', str, []),
        ],
    },

    # profile methods
    'profile': {
        'setXNML': [
            ('uid', int, ['optional']),
            ('profile', str, ['optional']),
            ('profile_action', str, ['optional']),
        ],

        'getXNML': [
            ('uid', int, ['optional']),
        ],
    },

    # users methods
    'users': { #namespace
        'getInfo': [ #method
            ('uids', list, []), #param_name, param_type, param_options
            ('fields', list, [('default', ['name'])]),
        ],

        'getLoggedInUser': [],

        'isAppAdded': [
            ('uid', int, ['optional']),
        ],
    },
    
    # invitations methods
	# @DaNmarner, @freefis
    'invitations': {
        'getOsInfo': [
            ('invite_ids',list,[]),
        ],
        'getUserOsInviteCnt': [
            ('uids',list,[]),
        ],
    },
    
    # admin methods
	# @DaNmarner, @freefis
    'admin': {
        'getAllocation':[],
    },
    
    #payment methods
    'pay': {
        'getToken': [
            ('order_id', int, []),
            ('amount', int, []),
        ],
        'isComplete': [
            ('order_id', int, []),
        ],
    },
}

class Proxy(object):
    """Represents a "namespace" of Xiaonei API calls."""

    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __call__(self, method, args=None, add_session_args=True):
        if add_session_args:
            self._client._add_session_args(args)
        logging.debug('auth proxy get called');
        return self._client('%s.%s' % (self._name, method), args)


# generate the Xiaonei proxies
def __generate_proxies():
    for namespace in METHODS:
        methods = {}

        for method in METHODS[namespace]:
            params = ['self']
            body = ['args = {}']

            for param_name, param_type, param_options in METHODS[namespace][method]:
                param = param_name

                for option in param_options:
                    if isinstance(option, tuple) and option[0] == 'default':
                        if param_type == list:
                            param = '%s=None' % param_name
                            body.append('if %s is None: %s = %s' % (param_name, param_name, repr(option[1])))
                        else:
                            param = '%s=%s' % (param_name, repr(option[1]))

                if param_type == json:
                    # we only jsonify the argument if it's a list or a dict, for compatibility
                    body.append('if isinstance(%s, list) or isinstance(%s, dict): %s = simplejson.dumps(%s)' % ((param_name,) * 4))

                if 'optional' in param_options:
                    param = '%s=None' % param_name
                    body.append('if %s is not None: args[\'%s\'] = %s' % (param_name, param_name, param_name))
                else:
                    body.append('args[\'%s\'] = %s' % (param_name, param_name))

                params.append(param)

            # simple docstring to refer them to Xiaonei API docs
            body.insert(0, '"""Xiaonei API call. See http://dev.xiaonei.com/wiki/%s.%s"""' % (namespace, method))

            body.insert(0, 'def %s(%s):' % (method, ', '.join(params)))

            body.append('return self(\'%s\', args)' % method)

            exec('\n    '.join(body))#turn IDL into functions

            methods[method] = eval(method)

        proxy = type('%sProxy' % namespace.title(), (Proxy, ), methods)

        globals()[proxy.__name__] = proxy


__generate_proxies()


class XiaoneiError(Exception):
    """Exception class for errors received from Xiaonei."""

    def __init__(self, code, msg, args=None):
        self.code = code
        self.msg = msg
        self.args = args

    def __str__(self):
        return 'Error %s: %s' % (self.code, self.msg)


class AuthProxy(Proxy):
    """Special proxy for xiaonei.auth."""

    def getSession(self):
        """Xiaonei API call. See http://dev.xiaonei.com/wiki/auth.getSession"""
        args = {}
        try:
            args['auth_token'] = self._client.auth_token
        except AttributeError:
            raise RuntimeError('Client does not have auth_token set.')
        result = self._client('%s.getSession' % self._name, args)
        self._client.session_key = result['session_key']
        self._client.uid = result['uid']
        self._client.secret = result.get('secret')
        self._client.session_key_expires = result['expires']
        return result

    def createToken(self):
        """Xiaonei API call. See http://dev.xiaonei.com/wiki/auth.createToken"""
        token = self._client('%s.createToken' % self._name)
        self._client.auth_token = token
        return token


class FriendsProxy(FriendsProxy):
    """Special proxy for xiaonei.friends."""

    def get(self, **kwargs):
        """Xiaonei API call. See http://dev.xiaonei.com/wiki/Friends.getFriends"""
        if self._client._friends:
            return self._client._friends
        return super(FriendsProxy, self).get(**kwargs)

class Xiaonei(object):
    """
    Provides access to the Xiaonei API.

    Instance Variables:

    added
        True if the user has added this application.

    api_key
        Your API key, as set in the constructor.

    app_name
        Your application's name, i.e. the APP_NAME in http://apps.xiaonei.com/APP_NAME/ if
        this is for an internal web application. Optional, but useful for automatic redirects
        to canvas pages.

    auth_token
        The auth token that Xiaonei gives you, either with xiaonei.auth.createToken,
        or through a GET parameter.

    callback_path
        The path of the callback set in the Xiaonei app settings. If your callback is set
        to http://www.example.com/xiaonei/callback/, this should be '/xiaonei/callback/'.
        Optional, but useful for automatic redirects back to the same page after login.

    internal
        True if this Xiaonei object is for an internal application (one that can be added on Xiaonei)

    page_id
        Set to the page_id of the current page (if any)

    secret
        Secret that is used after getSession for desktop apps.

    secret_key
        Your application's secret key, as set in the constructor.

    session_key
        The current session key. Set automatically by auth.getSession, but can be set
        manually for doing infinite sessions.

    session_key_expires
        The UNIX time of when this session key expires, or 0 if it never expires.

    uid
        After a session is created, you can get the user's UID with this variable. Set
        automatically by auth.getSession.

    ----------------------------------------------------------------------

    """

    def __init__(self, api_key, secret_key, auth_token=None, app_name=None, callback_path=None, internal=None, proxy=None):
        """
        Initializes a new Xiaonei object which provides wrappers for the Xiaonei API.

        For web apps, if you are passed an auth_token from Xiaonei, pass that in as a named parameter.
        Then call:

        xiaonei.auth.getSession()

        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.session_key = None
        self.session_key_expires = None
        self.auth_token = auth_token
        self.secret = None
        self.uid = None#
        self.page_id = None
        self.in_iframe = False
        self.added = False
        self.app_name = app_name
        self.callback_path = callback_path
        self.internal = internal
        self._friends = None
        self.proxy = proxy

        
        for namespace in METHODS:#injected all api calls here
            body = '%sProxy(self, \'%s\')' % (namespace.title(), 'xiaonei.%s' % namespace);
            self.__dict__[namespace] = eval('%sProxy(self, \'%s\')' % (namespace.title(), 'xiaonei.%s' % namespace))
            #logging.debug("Adding method?:%s , %s"%(namespace,body) );

        self.auth = AuthProxy(self, 'xiaonei.auth')
    def __str__(self):
        return "API_KEY:%s ||| SESSION_KEY:%s ||| UID%s ||| CALL_BACK_PATH:%s |||" \
                    %( self.api_key, self.session_key, self.callback_path, self.uid);
                

    def unicode_encode(self, str):
        """
        @author: houyr
        Detect if a string is unicode and encode as utf-8 if necessary
        """
        return isinstance(str, unicode) and str.encode('utf-8') or str

    def _hash_args(self, args, secret=None):
        """Hashes arguments by joining key=value pairs, appending a secret, and then taking the MD5 hex digest."""
        #@author: houyr
        #Fix for UnicodeEncodeError
        hasher = md5.new(''.join(['%s=%s' % (self.unicode_encode(x), self.unicode_encode(args[x])) for x in sorted(args.keys())]))
        if secret:
            hasher.update(secret)
        elif self.secret:
            hasher.update(self.secret)
        else:
            hasher.update(self.secret_key)
        return hasher.hexdigest()


    def _parse_response_item(self, node):
        """Parses an XML response node from Xiaonei."""
        # temp fix for friends_getAppUsers_response
        if node.nodeName == 'friends_getAppUsers_response':
            return self._parse_response_list(node)
        
        if node.nodeType == node.DOCUMENT_NODE and \
            node.childNodes[0].hasAttributes() and \
            node.childNodes[0].hasAttribute('list') and \
            node.childNodes[0].getAttribute('list') == "true":
            return {node.childNodes[0].nodeName: self._parse_response_list(node.childNodes[0])}
        elif node.nodeType == node.ELEMENT_NODE and \
            node.hasAttributes() and \
            node.hasAttribute('list') and \
            node.getAttribute('list')=="true":
            return self._parse_response_list(node)
        elif len(filter(lambda x: x.nodeType == x.ELEMENT_NODE, node.childNodes)) > 0:
            return self._parse_response_dict(node)
        else:
            #fix: xiaonei uses cdata section for user name in friends.getFriends
            return ''.join(node.data for node in node.childNodes if node.nodeType in [node.TEXT_NODE, node.CDATA_SECTION_NODE])


    def _parse_response_dict(self, node):
        """Parses an XML dictionary response node from Xiaonei."""
        result = {}
        for item in filter(lambda x: x.nodeType == x.ELEMENT_NODE, node.childNodes):
            result[item.nodeName] = self._parse_response_item(item)
        if node.nodeType == node.ELEMENT_NODE and node.hasAttributes():
            if node.hasAttribute('id'):
                result['id'] = node.getAttribute('id')
        return result


    def _parse_response_list(self, node):
        """Parses an XML list response node from Xiaonei."""
        result = []
        for item in filter(lambda x: x.nodeType == x.ELEMENT_NODE, node.childNodes):
            result.append(self._parse_response_item(item))
        return result


    def _check_error(self, response):
        """Checks if the given Xiaonei response is an error, and then raises the appropriate exception."""
        if type(response) is dict and response.has_key('error_code'):
            raise XiaoneiError(response['error_code'], response['error_msg'], response.get('request_args','no request_args found'))


    def _build_post_args(self, method, args=None):
        """Adds to args parameters that are necessary for every call to the API."""
        if args is None:
            args = {}

        for arg in args.items():
            if type(arg[1]) == list:
                args[arg[0]] = ','.join(str(a) for a in arg[1])
            elif type(arg[1]) == unicode:
                args[arg[0]] = arg[1].encode("UTF-8")

        args['method'] = method
        args['api_key'] = self.api_key
        args['v'] = '1.0'
        args['format'] = RESPONSE_FORMAT
        args['sig'] = self._hash_args(args)

        return args


    def _add_session_args(self, args=None):
        """Adds 'session_key' and 'call_id' to args, which are used for API calls that need sessions."""
        if args is None:
            args = {}

        if not self.session_key:
            return args
            #some calls don't need a session anymore. this might be better done in the markup
            #raise RuntimeError('Session key not set. Make sure auth.getSession has been called.')

        args['session_key'] = self.session_key
        args['call_id'] = str(int(time.time() * 1000))

        return args


    def _parse_response(self, response, method, format=None):
        """Parses the response according to the given (optional) format, which should be either 'JSON' or 'XML'."""
#        print 'Got response: %s' % response
        if not format:
            format = RESPONSE_FORMAT

        #Use XML for now
        if format == 'JSON':
            result = simplejson.loads(response)

            self._check_error(result)
        elif format == 'XML':
            dom = minidom.parseString(response)
            result = self._parse_response_item(dom)
            dom.unlink()

            if 'error_response' in result:
                self._check_error(result['error_response'])

            result = result[method[8:].replace('.', '_') + '_response']
        else:
            raise RuntimeError('Invalid format specified.')

        return result

    def unicode_urlencode(self,params):
        """
        @author: houyr
        A unicode aware version of urllib.urlencode
        """
        if isinstance(params, dict):
            params = params.items()
        return urllib.urlencode([(k, self.unicode_encode(v))
                          for k, v in params])

    def __call__(self, method, args=None, secure=False):
        """Make a call to Xiaonei's REST server."""
        #@author: houyr
        #Fix for bug of UnicodeEncodeError
        #post_data = urllib.urlencode(self._build_post_args(method, args))
        post_data = self.unicode_urlencode(self._build_post_args(method, args))
#        logging.debug('calling api with data: %s' % post_data)
        if self.proxy:
            proxy_handler = urllib2.ProxyHandler(self.proxy)
            opener = urllib2.build_opener(proxy_handler)
            if secure:
                response = opener.open(XIAONEI_SECURE_URL, post_data).read() 
            else:
                response = opener.open(XIAONEI_URL, post_data).read()
        else:
            if secure:
                response = urlread(XIAONEI_SECURE_URL, post_data)
            else:
                response = urlread(XIAONEI_URL, post_data)

        return self._parse_response(response, method)

    
    # URL helpers
    def get_url(self, page, **args):
        """
        Returns one of the Xiaonei URLs (www.xiaonei.com/SOMEPAGE).
        Named arguments are passed as GET query string parameters.

        """
        return 'http://www.xiaonei.com/%s.do?%s' % (page, urllib.urlencode(args))


    def get_app_url(self, path=''):
        """
        Returns the URL for this app's canvas page, according to app_name.
        
        """
        return 'http://apps.xiaonei.com/%s/%s' % (self.app_name, path)


    def get_add_url(self, next=None):
        """
        Returns the URL that the user should be redirected to in order to add the application.

        """
        args = {'api_key': self.api_key, 'v': '1.0'}

        if next is not None:
            args['next'] = next

        return 'http://app.xiaonei.com/apps/add.do?%s' % urllib.urlencode(args)


    def get_authorize_url(self, next=None, next_cancel=None):
        """
        Returns the URL that the user should be redirected to in order to authorize certain actions for application.

        """
        args = {'api_key': self.api_key, 'v': '1.0'}

        if next is not None:
            args['next'] = next

        if next_cancel is not None:
            args['next_cancel'] = next_cancel

        return self.get_url('authorize', **args)


    def get_login_url(self, next=None, popup=False, canvas=True):
        """
        Returns the URL that the user should be redirected to in order to login.

        next -- the URL that Xiaonei should redirect to after login

        """
        args = {'api_key': self.api_key, 'v': '1.0'}

        if next is not None:
            args['origURL'] = next
            
        if canvas is True:
            args['canvas'] = 1

        if popup is True:
            args['popup'] = 1

        if self.auth_token is not None:
            args['auth_token'] = self.auth_token

        return 'http://login.xiaonei.com/Login.do?%s' % urllib.urlencode(args)


    def login(self, popup=False):
        """Open a web browser telling the user to login to Xiaonei."""
        import webbrowser
        webbrowser.open(self.get_login_url(popup=popup))


    def check_session(self, request):
        """
        Checks the given Django HttpRequest for Xiaonei parameters such as
        POST variables or an auth token. If the session is valid, returns True
        and this object can now be used to access the Xiaonei API. Otherwise,
        it returns False, and the application should take the appropriate action
        (either log the user in or have him add the application).

        """
        self.in_iframe = (request.POST.get('xn_sig_in_iframe') == '1')

        if self.session_key and (self.uid or self.page_id):
            return True

        
        if request.method == 'POST':
            params = self.validate_signature(request.POST)
#            logging.debug('checksession, post params are: %s' % params)
        else:
            if 'installed' in request.GET:
                self.added = True

            if 'auth_token' in request.GET:
                self.auth_token = request.GET['auth_token']

                try:
                    self.auth.getSession()
                except XiaoneiError, e:
                    self.auth_token = None
                    return False

                return True

            params = self.validate_signature(request.GET)

        if not params:
            return False

        if params.get('in_iframe') == '1':
            self.in_iframe = True

        if params.get('added') == '1':
            self.added = True

        if params.get('expires'):
            self.session_key_expires = int(params['expires'])

        if 'friends' in params:
            if params['friends']:
                self._friends = params['friends'].split(',')
            else:
                self._friends = []

        if 'session_key' in params:
            self.session_key = params['session_key']
            if 'user' in params:
                self.uid = params['user']
            elif 'page_id' in params:
                self.page_id = params['page_id']
            else:
                return False
        else:
            return False

        return True


    def validate_signature(self, post, prefix='xn_sig', timeout=None):
        """
        Validate parameters passed to an internal Xiaonei app from Xiaonei.

        """
        args = post.copy()
        return dict([(key[len(prefix + '_'):], value) for key, value in args.items() if key.startswith(prefix)])
