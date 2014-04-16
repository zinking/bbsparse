
from django.core.management.base import BaseCommand
from optparse import make_option

from pageharvest.settings import *;
from pageharvest.disqus import *;
from pageharvest.blog import *;

import datetime;
import logging
import time

logger = logging.getLogger('bbs_dig')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-l', '--listposts',  dest='listposts', 
             help='list editor posts within hours'),
        make_option( '-s', '--sendposts',  dest='sendposts', 
             help='push editor blogs to microblogs'),
    )
    
    @staticmethod
    def list_editor_posts( hoursbefore ):
	ps = []
        try:
	    d = Disqus()
	    ps = d.listEditorPosts(hoursbefore,'asc')
        except Exception,e:
	    logger.error('LIST EDITOR POSTS FA:%s'%(e))
            raise e;
	return ps

    def handle(self,  **options):
        
        if options.get('listposts'):
	    hb = options.get('listposts')
            posts = Command.list_editor_posts( int(hb) )
	    for p in posts:
		logger.info('%s POSTED %s AT %s'%(p['author']['username'], p['postcontent'], p['createdAt']) )
        if options.get('sendposts'):
            hb = options.get('sendposts');
            posts = Command.list_editor_posts(int(hb))
	    try:
		robot = MblogRobot()
		for p in posts:
		    #robot.postMsg( p['postcontent'] , p['postlink'])
		    logger.info( p['postcontent'] + p['postlink']+'\n\n\n')
		    logger.info('POST BLOG SU:%s len:%d'%(p['postcontent'][0:10], len( p['postcontent'])))
		    #time.sleep(60)
	    except Exception,e:
		logger.error('POST BLOG FA:%s'%(e))

            
            
            

                                                
           
        
