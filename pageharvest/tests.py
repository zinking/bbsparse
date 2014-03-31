# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from pageharvest.disqus import *
from pageharvest.blog import *

class DisqusTestCase( SimpleTestCase):
    def setUp(self):
	self.d =  Disqus()

    def test_disqus_can_fetch( self ):
	posts =  self.d.fetchPostsSince( -2, 'desc')
	self.assertTrue( len(posts) > 1 )

    def test_disqus_can_filter( self ):
	#assuming I didn't comment just now
	posts =  self.d.fetchPostsSince( -0, 'asc' )
	self.assertTrue( len(posts) == 0 )


class MblogTestCase( SimpleTestCase ):
    def setUp(self):
	self.sb =  MblogRobot()
	

    def test_send_sina_mblg(self):
	resp = self.sb.postMsg('helloworld','')
	self.assertTrue( resp.url.find('sorry')  == -1 )

    def test_send_sina_full(self):
	text= u""" [博士][萌妹子]；
水仙花姐姐~~；
水木和求实挺同步啊； 
还是本科毕业好啊 
越来越有体会，把女人比作花多么贴切，绚丽的绽放后就是无情的凋零， 
当然目测水仙花还不算老。；
传说中的水仙花妹妹重现江湖 记得我刚上研究生时可火了  一晃5年过去了5年
	过去了 """

	link = "http://localhost:8000/content/go?l=6305"
	resp = self.sb.postMsg(text,link)
	self.assertTrue( resp.url.find('sorry')  == -1 )

    def test_send_sina_exceed(self):
	text= u""" [博士][萌妹子]；
水仙花姐姐~~；
水木和求实挺同步啊； 
还是本科毕业好啊 
越来越有体会，把女人比作花多么贴切，绚丽的绽放后就是无情的凋零， 
当然目测水仙花还不算老。；
传说中的水仙花妹妹重现江湖 记得我刚上研究生时可火了  一晃5年过去了5年
传说中的水仙花妹妹重现江湖 记得我刚上研究生时可火了  一晃5年过去了5年
传说中的水仙花妹妹重现江湖 记得我刚上研究生时可火了  一晃5年过去了5年
传说中的水仙花妹妹重现江湖 记得我刚上研究生时可火了  一晃5年过去了5年
水仙花姐姐~~；
水木和求实挺同步啊； 
还是本科毕业好啊 
越
	过去了 """

	link = "http://localhost:8000/content/go?l=6305"
	resp = self.sb.postMsg(text,link)
	self.assertTrue( resp.url.find('sorry')  == -1 )

