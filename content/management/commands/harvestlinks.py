from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option

import logging


from content.models         import *;
from pageharvest.settings   import *;
from pageharvest.bbsparser  import *;
from threading import Thread

logger = logging.getLogger('bbs_dig')

import datetime;

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-c', '--schoolcont',dest='harvest_count', help='by count'),
        make_option( '-s', '--schoolname',dest='harvest_school',help='by school'),
        make_option( '-u', '--updatecfg', dest='update_config', help='update'),
        make_option( '-d', '--deletelink',dest='delete_link',   help='delete'),
        make_option( '-t', '--tracesteps',dest='trace_steps',   help='trace'),
        make_option( '-p', '--probesteps',dest='probe_steps',   help='probe'),
    )

    def handle(self,  **options):
        if options.get('harvest_count'):
            schoolcount     =   int(options.get('harvest_count'))#options.harvest_count;
            currentcount    = 0;
	    sbpc_list = SBPC.objects.exclude( status=STATUS_UNREACHABLE ).order_by('rank');
	    for sbpc in sbpc_list :
		parser = BBSParser( sbpc );
		thread = Thread( target=parser.executepipeline, args=())
		thread.start()
		thread.join()
            
        if options.get('harvest_school'):
            bbsname = options.get('harvest_school');
            if options.get('update_config') is not None:
                from config import Command as ConfigCommand;
                ConfigCommand.update_schoolconfig(bbsname);
            if options.get('delete_link') is not None:
                from op     import Command as OperatCommand;
                OperatCommand.delete_schoollink(bbsname);

	    import pdb
	    #pdb.set_trace()
	    sbpc = SBPC.objects.get( bbsname=bbsname );
            if options.get('trace_steps') is not None:
		step = float( options.get('trace_steps'))
		parser = BBSParser( sbpc, 'debug')
		parser.executepipelinestep( step, True )
	    else:
		parser = BBSParser( sbpc, 'debug')
		parser.executepipeline( )
            
            

 
