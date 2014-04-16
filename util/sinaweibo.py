#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import urllib
import base64
import binascii
 
import rsa
import time
 
import logging

from spider import Spider
#logging.basicConfig(level=logging.DEBUG)
 
class SinaWeibo(object): 
    def __init__( self ):
	self.WBCLIENT = 'ssologin.js(v1.4.5)'
	self.session = Spider().session


    def encrypt_passwd( self, passwd, pubkey, servertime, nonce):
	key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
	message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
	passwd = rsa.encrypt(message, key)
	return binascii.b2a_hex(passwd)

    def post_weibo(self, text ):
	data = {
	    'text'      :text,
	    'location'  :'home',
	    'pic_id'    :'',
	    'rank'      :'0',
	    'rankid'    :'',
	    '_surl'     :'',
	    'hottopicid':'',
	    'location'  :'home',
	    'module'    :'stissue',
	    '_t'        :'0',
	}
	ts = long(time.time()*1000)
	self.session.headers['X-Request-With'] = 'XMLHttpRequest'
	resp = self.session.post(
	    'http://weibo.com/aj/mblog/add?_wv=5&__rnd=%s'%(str(ts)),
	    data=data
	)

	if resp.url.find( 'sorry') != -1:
	    raise Exception('POST BLOG FA, %s'%(resp.url))
	return resp

    def wblogin(self, username, password):
	resp = self.session.get(
	    'http://login.sina.com.cn/sso/prelogin.php?'
	    'entry=sso&callback=sinaSSOController.preloginCallBack&'
	    'su=%s&rsakt=mod&client=%s' %
	    (base64.b64encode(username), self.WBCLIENT)
	)

	pre_login_str = re.match(r'[^{]+({.+?})', resp.content).group(1)

	pre_login = json.loads(pre_login_str)
	data = {
	    'entry': 'weibo',
	    'gateway': 1,
	    'from': '',
	    'savestate': 7,
	    'userticket': 1,
	    'ssosimplelogin': 1,
	    'su': base64.b64encode(urllib.quote(username)),
	    'service': 'miniblog',
	    'servertime': pre_login['servertime'],
	    'nonce': pre_login['nonce'],
	    'vsnf': 1,
	    'vsnval': '',
	    'pwencode': 'rsa2',
	    'sp': self.encrypt_passwd(password, pre_login['pubkey'],
				 pre_login['servertime'], pre_login['nonce']),
	    'rsakv' : pre_login['rsakv'],
	    'encoding': 'UTF-8',
	    'prelt': '115',
	    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
		   'naSSOController.feedBackUrlCallBack',
	    'returntype': 'META'
	}
	resp = self.session.post(
	    'http://login.sina.com.cn/sso/login.php?client=%s' % self.WBCLIENT,
	    data=data
	)

	login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
			      resp.content).group(1)
	resp = self.session.get(login_url)
	#pat_to_extract_json_result
	pattern = r'\((.+?)\)'
	#pattern = r'[^{]+({.+?}})'
	login_str = re.search(pattern, resp.content).group(1)
	self.loginResult  = json.loads(login_str)
	#self.session.get( self.loginResult['redirect'])
	resp = self.session.get('http://weibo.com/')

	self.session.headers['Referer'] = resp.url 
	self.session.headers['Origin'] = 'http://weibo.com'
	self.session.headers['Host'] = 'weibo.com'
 
 
if __name__ == '__main__':
    from pprint import pprint
    #pprint(wblogin('XXXX@gmail.com', 'XXXX'))
    pass

	
