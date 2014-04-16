#! /usr/bin/env python
#-*- coding: utf-8 -*-

import requests
import logging

class Spider(object):
    def __init__( self ):
	user_agent = (
	    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
	    'Chrome/20.0.1132.57 Safari/536.11'
	)
	self.session = requests.session()
	self.session.headers['User-Agent'] = user_agent

	
