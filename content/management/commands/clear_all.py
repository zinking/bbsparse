"""
"""

from django.core.management.base import NoArgsCommand

from content.models         import *;
from pageharvest.settings   import *;

import datetime;


class Command(NoArgsCommand):
    help = "Clear all the Links & Configs in the DB"

    def handle_noargs(self, **options):
        sbpc_list = SBPC.objects.all();
        for sbpc in sbpc_list:
            sbpc.delete();
        print 'All Configs cleared';
        link_list = Links.objects.all();
        for link in link_list:
            link.delete();
        print 'All Links cleared';
            
           
        
