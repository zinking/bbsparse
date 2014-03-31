from bbsparse.settings import  *
from util.sinaweibo import *

import logging

class MblogRobot(object):
    def __init__(self):
	self.sina = SinaWeibo()
	login_result = self.sina.wblogin( SINA_163_USERNAME, SINA_163_PASSWORD )

    def postMsg(self, text , link ):
	text_quota = 250 - len(link)
	if len( text ) > text_quota:
	    text = text[0:text_quota]
	return self.sina.post_weibo( text+link )

	
