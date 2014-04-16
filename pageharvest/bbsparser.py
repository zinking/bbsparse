# coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from BeautifulSoup import BeautifulSoup;
from bsoupxpath import Path;
from customized_soup import CustomizedSoup;
from scraper import Scraper;
from util.spider import *

import htmlentitydefs;
import HTMLParser

import re,copy,string,time;
from datetime import *

import logging as logger


from pageharvest.settings import *;
from content.models       import *;


default_pipeline = {
    1.0:'fetchcontent',
    2.0:'extractblock',
    3.0:'scrapestruct',
    4.0:'fixdomdetail',
    5.0:'persisresult',
}

class BBSParser(object):

    def __init__( self ):
	self.session = Spider().session

    def setupexecontext(self, sbpc):
	pc = eval( sbpc.parseconfig )
	p  = default_pipeline 
	if pc.has_key('pipeline'):
	    p = p.extend( pc['pipeline'])
	return { 'sbpc':sbpc, 'pc':pc }

    def executepipeline(self, sbpc):
	t1 = time.time();
	context = self.setupexecontext(sbpc)
	for k in sorted( p.iterkeys()):
	    try:
		getattr( self, p[k] )( context )
	    except Execption,e:
		logstr = 'PIPE step %.2f %s FA: %s'%( float(k), p[k], e)
		logger.info( logstr )
	t2 = time.time()
        delta = (t2-t1)*1000;
        sbpc.totalparsetime = sbpc.totalparsetime + delta;
	logstr = "%s PIPE SU in %d millis" %( pc['bbsname'] , delta )
	logger.info( logstr )
        sbpc.lastfresh = datetime.now();
        sbpc.status = STATUS_NORMAL;
        sbpc.save();


    def fetchcontent(self, context ):
	from requests.exceptions import *
	sbpc = context['sbpc']; pc = context['pc']
	logstr = 'FETCH CONTENT %s '%( sbpc.bbsname )
	htmlstring = ""
        try: 
	    htmlstring = self.session.get( pc['locate'], timeout=2 ).content
	    sbpc.parse_su()
        except Timeout, e: 
	    sbpc.parse_fa()
	    logstr += "timeout %s" %( pc['bbsname'])
            logger.error( logstr );
	    raise e
        encoding = pc['encoding'] if ( pc.has_key('encoding') )else 'GBK' 
        htmlstring = unicode(htmlstring, encoding, 'ignore').encode('utf8');
	context['htmlstring'] = htmlstring

    def extractblock( self, context ):
	htmlstring = context['htmlstring']
	reblock = re.compile( context['pc']['re'], re.DOTALL)
	result  = reblock.search( context['htmlstring'])
	if result is None : raise Exception('extract block NONE')
	blockstr= result.group()
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

    def fixdomdetail(self, context ):
	items = context['items']
	pc    = context['pc']
	#for item in items: self.fixitem( item, pc )
	map( lambda i:self.fixitem(i,pc), items)

    def persisresult( self, context ):
	items = context['items']
	sbpc  = context['sbpc']
	newc  = 0
	for item in items: newc += Link.saveorupdate( item, sbpc )
	logstr = " %d of %d new links persisted"%( newc, len(items))

	
	

    
    def convertdom2string(self, domlist):
        list_str = u'';
        for i in range(len(domlist)):
            list_str += unicode(domlist[i]);
        return list_str;

    def save_parsed_links(self, linklist , pc, sbpc ):
        for link in linklist:
            try:
                linkobj = Link.objects.get( titlelink=link['titlelink'] );
                linkobj.updatetime = datetime.now();
                linkobj.save();
                info = 'existing links updated %s' %(linkobj)
                logger.debug( info );
            except Link.DoesNotExist:
                    nlinkobj = Link( createtime=datetime.now(), updatetime=datetime.now(), school=sbpc  );
                    for k,v in link.items():
                        setattr( nlinkobj, k, v )
                    nlinkobj.save();
                    info = 'new links fetched %s' %(nlinkobj)
                    logger.debug( info );
                    sbpc.lastrefresh = datetime.now();
                    sbpc.save();
            except Exception,e:
                info = 'CAUGHT EXCEPTION %s'%( e )
                logger.error( info );

    """
    PARSING BBS USING PREDEFINED PARSING CONFIGURATIONS
    """
    def parsebbs(self, sbpc ):#parsepc
        t1 = time.time();
        pc = eval( sbpc.parseconfig );
        logger.debug( 'parsing sbpc %s'%(sbpc) ); 
        try: 
	    htmlstring = self.session.get( pc['locate'] ).content
	    sbpc.parse_su()
        except Exception, e: 
	    sbpc.parse_fa()
            info = "Failed to open following url %s of school: %s" % (pc['locate'], pc['bbsname']);
            logger.error( info );
            return 0;
        encoding = pc['encoding'] if ( pc.has_key('encoding') )else 'GBK' 
        htmlstring = unicode(htmlstring, encoding, 'ignore').encode('utf8');
        try:
            if( pc['type'] == PARSE_USE_XPATH ):
                linklist = self.parsebbsbyXpath(pc,htmlstring);           
            else:
                linklist = self.parsebbsbyRegularExpression(pc,htmlstring);
        except Exception, e:
            info = "Exception:SITE changed; schoolname= %s :%s"%( pc['bbsname'],e )
            logger.error( info );
            sbpc.status = STATUS_EXCEPTION;
            sbpc.save();
            return 0
        t2 = time.time();
            
        self.save_parsed_links(linklist, pc, sbpc );
        delta = (t2-t1)*1000;
        sbpc.totalparsetime = sbpc.totalparsetime + delta;
        logger.debug("Successfully parsing school:%s costing %d milliseconds;" % (pc['bbsname'], delta ));
        sbpc.lastfresh = datetime.now();
        sbpc.status = STATUS_NORMAL;
        sbpc.save();
        return delta;


    def parsebbsbyXpath(self, pc, htmlstring):
        logger.debug( 'parsing using XPATH' );
        try:
            dom = BeautifulSoup(htmlstring);
        except Exception, e:
            info = "Xpath parsing exception school:%s %s"%( pc['bbsname'],e);
            logger.error( info );
            raise Exception(info);
        contentpath = Path(pc['xpath']);
        domblock = contentpath.apply(dom);
        blockstring = self.convertdom2string(domblock) ;

        return self.parsebbsDomDetail(blockstring, pc);
    
    def parsebbsbyRegularExpression(self, pc, htmlstring):
        logger.debug( 'parsing using regular expression' );
        try:
            re_block = re.compile( pc['re'], re.DOTALL);
            #print pc['re']
            #print len( htmlstring )
            blockstring = re_block.search(htmlstring).group();
            #logger.debug( blockstring );
        except Exception, e:
            info = "RE parser exception school %s %s"%( pc['bbsname'],e);
            logger.error( info ); 
            raise Exception(info);
        return self.parsebbsDomDetail(blockstring, pc);
    
    #TBD finish this in a more reasonable way
    def fixitem(self, item , pc):
        orginal_link = item['titlelink'];
        item['titlelink'] = pc['root'] + item['titlelink'];
        if ( 'additional' in pc.keys() and pc['additional'] == 'special' ):
            item['titlelink'] = pc['root'] %( item['board'],orginal_link);
        if ('re_board' in pc.keys()):
            re_board = re.compile( pc[ 're_board' ], re.DOTALL);
            titlegroup = re_board.search(item['title']);
            item['board'] = titlegroup.group('board');
            item['title'] = titlegroup.group('title');
        if ( 'pat_board_from_titlelink' in pc.keys() ):
            re_board_from_titlelink = re.compile( pc[ 'pat_board_from_titlelink' ], re.DOTALL);
            match_group = re_board_from_titlelink.search(item['titlelink']);
            item['board'] = match_group.group('board')
        
            
    #return links list
    def parsebbsDomDetail(self, dom_block_str , pc):     
        try:
            dom_row_pattern = pc['dom_row_pattern']; 
            #make dom block string become dom again, 
            #Unreasonable for: string->dom->blockdom->blockstring->blockdom->rowdom->rowstring need to be revised
            doc = CustomizedSoup(dom_block_str);        
            scraper = Scraper(dom_row_pattern);         #setup scraper to scrape row string
            ret = scraper.match(doc);
            if len(ret) == 0:
                raise Exception("0 RESULTS RETURNED FROM ROW PATTERN, ROW PATTERN BROKE");
            retlength = min( len(ret),10);
            ret = ret[0:retlength];
            parsed_result = []; 
            info = "totally %d items parsed for school %s " %( len(ret), pc['locate'] );
            logger.info( info );
            for item in ret:
                value = scraper.extract(item); 
                value['titlelink'] = h.unescape( value['titlelink'] );
                self.fixitem(value, pc);
                #value['title'] = unescape( value['title'] );#SAFE TITLE
                parsed_result.append(value);
        except Exception, e: 
            info = "Dom detail exception: school %s %s \n"%( pc['locate'], e );
            info += "LENGHT OF DOCSTR %d"%(len(dom_block_str))
            logger.error( info ); 
            raise Exception(info);
        
        #logger.debug( parsed_result ); 
        return  parsed_result;
        
        
