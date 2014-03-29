"""
"""

from django.core.management.base import NoArgsCommand
from content.models         import *;
from pageharvest.settings   import *;
from django.core.exceptions import ObjectDoesNotExist

import datetime;
import logging

logger = logging.getLogger('bbs_dig')

class Command(NoArgsCommand):
    help = "Setup Initial SPBC Configuration into the DB"

    def handle_noargs(self, **options):
    
        #objs = SBPC.objects.all()
        #for obj in objs:
        #    obj.delete(); this is not going to work because it will break the refrence integrity
        for bc in bbs_setting_list :
            try:
                sbpc = SBPC.objects.get( bbsname = bc['bbsname'] )
                #sbpc.schoolname = bc['schoolname']
                #sbpc.rank = bc['rank']
                #sbpc.chinesename = bc['chinesename']
                sbpc.parseconfig = bc
                if bc.has_key('status') : sbpc.status = bc['status'];
                sbpc.save()
                logger.info( 'update config for bbs %s, %s' %( bc['bbsname'], bc ) )
            except ObjectDoesNotExist:
                #if object does not exist then create
                sbpc = SBPC( bbsname = bc['bbsname'], schoolname = bc['schoolname'],
                    rank = bc['rank'], chinesename = bc['chinesename'], 
                    parseconfig = bc );
                if bc.has_key('status') : sbpc.status = bc['status'];
                sbpc.save();
                logger.info( 'added config for bbs %s, %s' %( bc['bbsname'], bc ) )
            except Exception,e:
                logger.error('Exception Occured when updating parse config %s'%(e) )
        logger.info( 'All SBPC Configuration setup successfully' )
           
        
