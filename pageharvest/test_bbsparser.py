# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from mock_django.models import ModelMock
from pageharvest.bbsparser import *
from pageharvest.settings import sjtubbs

class BbsparserTestCase( SimpleTestCase):
    def setUp(self):
	self.sbpc = ModelMock(SBPC)
	self.sbpc.parseconfig = repr(testbbs)
	self.parser = BBSParser(self.sbpc)
	self.ctx = self.parser.setupexecontext( )
	

    def test_fetchcontent( self ):
	self.parser.fetchcontent( self.ctx )
	self.assertTrue( self.ctx.has_key('htmlstring'))

    def test_fetchcontentfa( self ):
	from requests.exceptions import *
	old = self.ctx['pc']['locate']
	self.ctx['pc']['locate'] = 'http://great-way.appspot.com'
	self.assertRaises( Timeout, self.parser.fetchcontent, self.ctx )
	self.ctx['pc']['locate'] = old

    def test_extractblock( self ):
	self.ctx['htmlstring']= u'<td valign="middle"><font color="#FFFFFF"><img src="iconT.gif"> <b>blahblahblah</b></font></td>\n                                </tr>\n                \t\t</table>\n                \t</td>\n                  </tr>blahblahblah</table>'

	self.parser.extractblock(self.ctx )
	self.assertTrue( self.ctx.has_key('blockstr') )

    def test_extractblockfa(self):
	self.ctx['htmlstring']= ""
	self.assertRaises( Exception, self.parser.extractblock, self.ctx )

    def test_scrapestruct(self):
	self.ctx['blockstr'] =  """    
       <td align="center" bgcolor="#f6f6f6" > <table width="100%" border="0" cellpadding="5" cellspacing="0">
                      <tr>
                        <td valign="top">
			    <table width=100% border=0><tr><td width=110>[<a
		href="/bbsdoc?board=Bowling"
		target="_self">     Bowling</a>]</td><td><a
		href="/bbstcon?board=Bowling&reid=1366905812"
		target="_self">[]Strike[]——xiaopangzi
		</a></td><td
		width=110>xiaopangzi</td></tr> """
	self.parser.scrapestruct( self.ctx )
	self.assertTrue( self.ctx.has_key('items'))
	self.assertTrue( len(self.ctx['items']) > 0 )
	headitem = self.ctx['items'][0]
	self.assertTrue( headitem.has_key('author'))

    def test_scrapestructfa(self):
	self.ctx['blockstr']= ""
	self.assertRaises( Exception, self.parser.extractblock, self.ctx )

    def test_regularparse(self):
	self.ctx['blockstr'] = """
	author1|board1|link1|title1;
	author1|board1|link1|title1;
	author1|board1|link1|title1;
	author1|board1|link1|title1;
	"""
	self.ctx['pc']['re_row'] = "(?P<author>\w+)\|(?P<board>\w+)\|(?P<link>\w+)\|(?P<title>\w+);"
	self.parser.regularparse(self.ctx )
	self.assertTrue( self.ctx.has_key('items'))
	items = self.ctx['items']
	self.assertTrue( len(items)==4 )
	head  = items[0]
	self.assertTrue( head.has_key('board') )

    def test_extractblock(self):
	self.ctx['htmlstring'] = "aaa<s>s1</s><s>s2</s>bbb"
	old = self.ctx['pc']['re']
	self.ctx['pc']['re'] = "<s>.*?</s>"
	self.parser.extractblock( self.ctx )
	self.assertTrue( self.ctx['blockstr'] == '<s>s1</s><s>s2</s>')
	self.ctx['pc']['re'] = old

    def test_regularparseuni(self):
	self.ctx['blockstr'] = u"""
	author1于|board1|link1|title1;
	author1于|board1|link1|title1;
	author1于|board1|link1|title1;
	author1于|board1|link1|title1;
	"""
	self.ctx['pc']['re_row'] = u"(?P<author>\w+)于\|(?P<board>\w+)\|(?P<link>\w+)\|(?P<title>\w+);"
	self.parser.regularparse(self.ctx )
	self.assertTrue( self.ctx.has_key('items'))
	items = self.ctx['items']
	self.assertTrue( len(items)==4 )
	head  = items[0]
	self.assertTrue( head.has_key('board') )

    def test_regularparseunifa(self):
	self.ctx['blockstr'] = u"""
	"""
	self.ctx['pc']['re_row'] = u"(?P<author>\w+)于\|(?P<board>\w+)\|(?P<link>\w+)\|(?P<title>\w+);"
	self.assertRaises( Exception, self.parser.extractblock, self.ctx )

    
    def test_pipeline(self):
	self.ctx = self.parser.executepipeline( )
	self.assertTrue( self.ctx.has_key('items'))
	items = self.ctx['items']
	self.assertTrue( len(items)>0 )
	headitem = items[0]
	self.assertTrue( headitem.has_key('author'))
	
    def test_cleanhtml(self):
	text = "<a>a link title</a>"
	t1 = self.parser.cleanuphtmltext(text)
	self.assertTrue( t1 == "a link title")
	t2 = "&pound;682m"
	t3 = self.parser.cleanuphtmltext(t2)
	self.assertTrue( t3 == "£682m")




