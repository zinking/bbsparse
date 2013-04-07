"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``RegistrationProfile.objects.delete_expired_users()``, which
contains the actual logic for determining which accounts are deleted.

"""

from django.core.management.base import BaseCommand
from optparse import make_option

from content.models         import *;
from pageharvest.settings   import *;

import datetime;


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-l', '--listfailed',  dest='listfailed', 
             help='list school with error status'),
        make_option( '-m', '--marknormal',  dest='marknormal', 
             help='mark innormal school into normal'),
        make_option( '-d', '--deleteschoollink',  dest='deletelink', 
             help='deletelinksofsomeschool'),
    )


    def handle(self,  **options):
        
        if options.get('listfailed'):
            failed = SBPC.objects.filter( status__gt = 1 );
            print 'listing school parse config with innormal status ';
            print 'TBD';
                
        if options.get('marknormal'):
            schoolname = options.get('marknormal');
            qschool = SBPC.objects.get( bbsname = schoolname );
            qschool.status = 1;
            qschool.save();
            print 'school back into normal now';
        if options.get('deletelink'):
            pass;#TBD
            
            
            

                                                
           
        
