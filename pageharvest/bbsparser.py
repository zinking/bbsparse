# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from BeautifulSoup import BeautifulSoup;
from bsoupxpath import Path;
from customized_soup import CustomizedSoup;
from scraper import Scraper;
from util.spider import Spider

import htmlentitydefs;
import HTMLParser

import re,copy,string;
from datetime import datetime
import cPickle

import logging as logger
logger.basicConfig(level=logger.DEBUG)


from pageharvest.settings import *;
from content.models       import *;
import time


default_pipeline = {
    1.0:'fetchcontent',
    2.0:'extractblock',
    3.0:'scrapestruct',
    4.0:'fixdomdetail',
    5.0:'persisresult',
}

class BBSParser(object):

    def __init__( self , sbpc, mode = 'normal' ): 
	self.session = Spider().session
	self.mode    = mode 
	self.sbpc    = sbpc
	self.htmlp   = HTMLParser.HTMLParser()

    def cleanuphtmltext(self,text):
	t1 = self.htmlp.unescape( text )
	return re.sub('<[^<]+?>', '', t1)
	
    def setupexecontext(self):
	pc = eval( self.sbpc.parseconfig )
	p  = default_pipeline 
	self.logstr = self.sbpc.bbsname + ' '
	if pc.has_key('pipeline'):
	    p.update( pc['pipeline'])
	return { 'pc':pc , 'p':p}

    def persistscontext(self, context):
	with open("persistscontext","w") as file:
	    file.write(cPickle.dumps(context))
    
    def loadpersistfile(self):
	with open("persistscontext","r") as file:
	    data = file.read()
	    return cPickle.loads(data)
	
    def executepipelinestep(self, step , trace = False ):
	import pdb
	if self.mode != 'debug' : return
	context = self.loadpersistfile()
	p = context['p']; 
	if( trace ): pdb.set_trace()
	getattr(self, p[step])(context)

    def executepipeline(self):
	t1 = time.time();
	context = self.setupexecontext()
	p = context['p']; pc=context['pc']
	for k in sorted( p.iterkeys()):
	    try:
		getattr( self, p[k] )( context )
		#logstr = self.logstr + 'PIPE step %.2f %s EXE'%( float(k), p[k])
		#if( self.mode == 'debug' ): logger.debug(logstr)
	    except Exception,e:
		logstr = self.logstr + 'PIPE step %.2f %s FA: %s'%( float(k), p[k], e)
		logger.info( logstr )
		context['result'] = 'FA'
		context['error'] = logstr
		if( self.mode =='debug') : self.persistscontext(context )
		return context
	t2 = time.time()
        delta = (t2-t1)*1000;
        self.sbpc.totalparsetime = self.sbpc.totalparsetime + delta;
	logstr = self.logstr + "%s PIPE SU in %d millis" %( pc['bbsname'] , delta )
	logger.info( logstr )
        self.sbpc.lastfresh = datetime.now();
        self.sbpc.status = STATUS_NORMAL;
        self.sbpc.save();
	if( self.mode == 'debug' ) : self.persistscontext(context)
	return context


    def fetchcontent(self, context ):
	from requests.exceptions import *
	pc = context['pc']
	htmlstring = ""
        try: 
	    htmlstring = self.session.get( pc['locate'], timeout=2 ).content
	    self.sbpc.parse_su()
        except Timeout, e: 
	    logstr = self.logstr + 'FETCHCONTENT %s '%( self.sbpc.bbsname )
	    self.sbpc.parse_fa()
	    logstr += "timeout %s" %( pc['bbsname'])
            logger.error( logstr );
	    raise e
        encoding = pc['encoding'] if ( pc.has_key('encoding') )else 'GBK' 
        htmlstring = unicode(htmlstring, encoding, 'ignore').encode('utf8');
	context['htmlstring'] = htmlstring

    def extractblock( self, context ):
	htmlstring = context['htmlstring']
	reblock = re.compile( context['pc']['re'], re.DOTALL)
	resultiter  = reblock.finditer( context['htmlstring'])
	resultlist  = list(resultiter)
	if len( resultlist ) == 0: raise Exception('extract block NONE')
	#blockstr= result.group()
	resultstrlist = map( lambda x:x.group(),resultlist )
	blockstr = reduce( lambda x,y:x+y, resultstrlist )
	context['blockstr'] = blockstr
	
    def scrapestruct(self, context ):
	pc = context['pc']
	rowscrape = pc['dom_row_pattern']
	blockstr  = context['blockstr']
	soupdoc   = CustomizedSoup( blockstr )
	scraper   = Scraper( rowscrape )
	results   = scraper.match( soupdoc )
	if( len(results) == 0 ): #TBD scraper need to be imporved
	    raise Exception("0 ITEMS SCRAPED WARNING")
	count = min(len(results), 10 )
	items     = results[0:count]
	eitems    = map( lambda i:scraper.extract(i), items)
	context['items'] = eitems

    def regularparse(self, context ):
	pc = context['pc']
	repat = re.compile(pc['re_row'], re.DOTALL|re.U|re.I)
	blockstr  = context['blockstr']
	resultiter   =  repat.finditer( blockstr ) 
	results = list( resultiter )
	if( len(results) == 0 ): #TBD scraper need to be imporved
	    raise Exception("0 ITEMS SCRAPED WARNING")
	count = min(len(results), 10 )
	items     = results[0:count]
	eitems    = map( lambda i:i.groupdict(), items)
	context['items'] = eitems

    def fixdomdetail(self, context ):
	items = context['items']
	pc    = context['pc']
	#for item in items: self.fixitem( item, pc )
	map( lambda i:self.fixitem(i,pc), items)

    def persisresult( self, context ):
	items = context['items']; newc  = 0
	for item in items: newc += Link.saveorupdate( item, self.sbpc )
	logstr = self.logstr + " %d of %d new links persisted"%( newc, len(items))
	logger.info( logstr )

   
    def fixitem(self, item , pc):
        orginal_link = item['titlelink'];
        item['titlelink'] = pc['root'] + item['titlelink'];
	if not isinstance( item['title'], basestring ):
	    titlelist = map( lambda x:x.string, item['title'] )
	    titletext = "".join( titlelist )
	    item['title'] = self.cleanuphtmltext( titletext ) 
        if ( 'additional' in pc.keys() and pc['additional'] == 'special' ):
            item['titlelink'] = pc['root'] %( item['board'],orginal_link);

	if ( 'additional' in pc.keys() and pc['additional'] == 'special2' ):
            item['titlelink'] = pc['root'] %( item['boardlink'],orginal_link);

        if ('re_board' in pc.keys()):
            re_board = re.compile( pc[ 're_board' ], re.DOTALL);
            titlegroup = re_board.search(item['title']);
            item['board'] = titlegroup.group('board');
            item['title'] = titlegroup.group('title');
        if ( 'pat_board_from_titlelink' in pc.keys() ):
            re_board_from_titlelink = re.compile( pc[ 'pat_board_from_titlelink' ], re.DOTALL);
            match_group = re_board_from_titlelink.search(item['titlelink']);
            item['board'] = match_group.group('board')
        
       
        
