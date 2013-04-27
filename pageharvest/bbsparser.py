# coding=utf-8
from datetime import *;

from BeautifulSoup import BeautifulSoup;
from bsoupxpath import Path;
from customized_soup import CustomizedSoup;
from scraper import Scraper;

import htmlentitydefs;

import re,copy,string,logging,time;
import urllib,urllib2,Cookie;

logger = logging.getLogger('bbs_dig')

from pageharvest.settings import *;
from content.models       import *;

def report_parse_exceptions( content ):
    logger.error("Reporting parse problems to administrators" );
    mail.send_mail(sender="BBS TOP 10<bbstop10@appspot.com>",
      to="Albert <zinking3@gmail.com>",
      subject="Parsing Problem Report - BBSTOP10",
      body=content)
      
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

class BBSParser(object):
    
    def convertdom2string(self, domlist):
        list_str = u'';
        for i in range(len(domlist)):
            list_str += unicode(domlist[i]);
        return list_str;

    def save_parsed_links(self, linklist , pc, sbpc ):
        #schoolbbs = get_object(Schoolbbs, 'schoolname =', pc['schoolname']);
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
            htmlstring = urllib2.urlopen( pc['locate'] ).read();
            sbpc.totalparse = sbpc.totalparse + 1;
            sbpc.rank = sbpc.rank - 1;
        except Exception, e: 
            sbpc.failedparse = sbpc.failedparse + 1;
            info = "Failed to open following url %s of school: %s" % (pc['locate'], pc['bbsname']);
            logger.error( info );
            #print info;
            sbpc.save();
            return 0;
        if ( not pc.has_key('encoding') ): htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('utf8');
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
            return 0;
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
            #import pdb
            #pdb.set_trace();
            for item in ret:
                value = scraper.extract(item); 
                self.fixitem(value, pc);
                value['title'] = unescape( value['title'] );#SAFE TITLE
                parsed_result.append(value);

        except Exception, e: 
            info = "Dom detail exception: school %s %s \n"%( pc['locate'], e );
            info += "LENGHT OF DOCSTR %d"%(len(dom_block_str))
            logger.error( info ); 
            raise Exception(info);
        
        #logger.debug( parsed_result ); 
        return  parsed_result;
        
        
