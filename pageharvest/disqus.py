from bbsparse.settings import *

from disqusapi import DisqusAPI
from datetime  import datetime,timedelta
import time

class Disqus(object):
    def __init__(self):
	self.disqus = DisqusAPI( DISQUS_SECRET, DISQUS_PUBLIC)

    def fetchPostsSince( self, hh, order ):
	if ( hh > 0 ) : hh *= -1
	chk = datetime.now() + timedelta(hours=hh) 
	uxk = time.mktime( chk.timetuple() )
	ts  = str(int(uxk))
	posts = self.disqus.posts.list( forum=DISQUS_APP,since=ts, order=order)
	return posts



    def listEditorPosts(self, hh, od):#deafult will be asc
	posts = self.fetchPostsSince( hh, od )
	if len(posts) == 0 : 
	    raise Exception('0 RESULTS FOUND')
	posts = filter( lambda x:x['author']['username'] in DISQUS_EDITOR , posts)
	for p in posts:
	    p['threadcontent'] = self.disqus.threads.details(thread=p['thread'])
	    msg = p['threadcontent']['clean_title'] + '|' + p['raw_message']
	    p['postcontent'] = msg
	    p['postlink'] = p['threadcontent']['link']
	return posts
	
