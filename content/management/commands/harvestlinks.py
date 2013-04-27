from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option

import logging


from content.models         import *;
from pageharvest.settings   import *;
from pageharvest.bbsparser  import *;

logger = logging.getLogger('bbs_dig')

import datetime;

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-c', '--schoolcount',  dest='harvest_count', 
             help='harvest school links of specified count'),
        make_option( '-s', '--schoolname',   dest='harvest_school', 
             help='harvest school links of specified school'),
        make_option( '-u', '--updateconfig', dest='update_config', 
             help='harvest school links of specified school'),
    )

    def handle(self,  **options):
        parser          =   BBSParser();
        if options.get('harvest_count'):
            schoolcount     =   int(options.get('harvest_count'))#options.harvest_count;
            currentcount    = 0;
            try:
                sbpc_list = SBPC.objects.all().order_by('rank');
                for sbpc in sbpc_list :  parser.parsebbs( sbpc );
            except Exception,e:
                raise e;
            
        if options.get('harvest_school'):
            bbsname = options.get('harvest_school');
            if options.get('update_config') is not None:
                from config import Command as ConfigCommand;
                ConfigCommand.update_schoolconfig(bbsname);
            try:
                logger.debug( 'parsing %s'%(bbsname) );
                sbpc = SBPC.objects.get( bbsname=bbsname );
                parser.parsebbs( sbpc  );
            except Exception,e:
                raise e;
            
            

 
