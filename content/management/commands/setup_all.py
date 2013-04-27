"""
"""

from django.core.management.base import NoArgsCommand
from content.models         import *;
from pageharvest.settings   import *;

import datetime;


class Command(NoArgsCommand):
    help = "Setup Initial SPBC Configuration into the DB"

    def handle_noargs(self, **options):
    
        objs = SBPC.objects.all()
        for obj in objs:
            obj.delete();
        for bc in bbs_setting_list :
            try:
                sbpc = SBPC( bbsname = bc['bbsname'], schoolname = bc['schoolname'],
                    rank = bc['rank'], chinesename = bc['chinesename'], 
                    parseconfig = bc );
                if bc.has_key('status') : sbpc.status = bc['status'];
                sbpc.save();
            except Exception,e:
                print e;
        print 'All SBPC Configuration setup successfully';
           
        
