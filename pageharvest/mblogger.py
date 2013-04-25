# coding=utf-8

__author__ = "zinking3@gmail.com"
__version__ = "0.1"
__license__ = "GPL"

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


from google.appengine.api import *
from datetime import *;

from BeautifulSoup import BeautifulSoup;
from bsoupxpath import Path;
from customized_soup import CustomizedSoup;
from scraper import Scraper;

import htmlentitydefs;

import re,copy,string,logging,time;
import urllib,urllib2,Cookie;

from pageharvest.settings import *;
from content.models       import *;


def unescape(text):
   """Removes HTML or XML character references 
      and entities from a text string.
      keep &amp;, &gt;, &lt; in the source code.
   from Fredrik Lundh
   http://effbot.org/zone/re-sub.htm#unescape-html
   """
   def fixup(m):
      text = m.group(0)
      if text[:2] == "&#":
         # character reference
         try:
            if text[:3] == "&#x":
               return unichr(int(text[3:-1], 16))
            else:
               return unichr(int(text[2:-1]))
         except ValueError:
            #print "erreur de valeur"
            pass
      else:
         # named entity
         try:
            if text[1:-1] == "amp":
               text = "&amp;amp;"
            elif text[1:-1] == "gt":
               text = "&amp;gt;"
            elif text[1:-1] == "lt":
               text = "&amp;lt;"
            else:
               #print text[1:-1]
               text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
         except KeyError:
            #print "keyerror"
            pass
      return text # leave as is
   return re.sub("&#?\w+;", fixup, text)

def make_cookie_header(cookie):
    ret = ""
    for val in cookie.values():
        ret+="%s=%s; "%(val.key, val.value)
    return ret

from util import twitter;
from util import bitly;
class Microblog(object):
    def __init__(self): 
        self.name = SINA_163_USERNAME;
        self.password = SINA_163_PASSWORD;
        self.skip_n163 = False;
        self.skip_sina = False;
        self.skip_twitter = False;
        
        self.login_to_sina_microblog();
        self.login_to_net163_microblog();

        self.twitter_api = twitter.Api(username=TWITTER_API_USERNAME, password=TWITTER_API_PASSWORD);
        self.bitly_api   =  bitly.Api(login=BITLY_API_USERNAME, apikey=BITLY_API_APIKEY); 

        result = 5;
        if( self.skip_n163 ): result -= 2;
        if( self.skip_sina ): result -= 2;
        if( self.skip_twitter ): result -=2;
        self.quota = result;

    

    def login_to_sina_microblog(self):
        try:
            self.sinahttp = urlfetch.fetch(
                url="https://login.sina.com.cn/sso/login.php?username=%s&password=%s&returntype=TEXT"%(self.name,self.password));
        except Exception,e:
            self.skip_sina = True;
            logging.error( "ERROR OCCURED WHEN logging to sina mblog " + str(e) );
        self.sinacookie = Cookie.SimpleCookie(self.sinahttp.headers.get('set-cookie', ''));#TBD
    def login_to_net163_microblog(self):
        try:
            self.n163http = urlfetch.fetch(
                url="https://reg.163.com/logins.jsp?username=%s&password=%s&product=t&type=1"%(self.name,self.password));
        except Exception,e:
            self.skip_n163 = True;
            logging.error( "ERROR OCCURED WHEN logging to 163 mblog " + str(e) );
        self.n163cookie = Cookie.SimpleCookie(self.n163http.headers.get('set-cookie', ''));
        
    def post_n163_msg(self,msg):
        if( self.skip_n163 ): return;
        msg=unescape(msg)
        form_fields = {
          "status": msg,          
        }
        form_data = urllib.urlencode(form_fields);
        try:
            result = urlfetch.fetch(url="http://t.163.com/statuses/update.do",
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Referer':'http://t.163.com','Cookie' : make_cookie_header(self.n163cookie)})
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN SENDING MBLOG TO 163 " + str(e) );

        
    def post_sina_msg(self, msg ):
        if( self.skip_sina ): return;       
        msg=unescape(msg);
        form_fields = {
          "content": msg,          
        }
        form_data = urllib.urlencode(form_fields)
        
        try:
            result = urlfetch.fetch(url="http://t.sina.com.cn/mblog/publish.php",
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Referer':'http://t.sina.com.cn','Cookie' : make_cookie_header(self.sinacookie)})
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN SENDING MBLOG TO SINA " + str(e) );
        

    
    def post_twitter_msg(self, item ):
        short_url = item['link'];
        try:
            short_url = self.bitly_api.shorten( item['link'] );
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN SHORTENING URL WITH BITLY " + str(e) );
            return;
        msg=item['pattern'] %( item['schoolname'], item['title'], short_url, item['author'] );
        msg=unescape(msg);
        try:
            self.twitter_api.PostUpdate( msg );
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN POSTING MBLOG TO TWITTER " + str(e) );