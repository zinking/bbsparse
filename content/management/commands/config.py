# coding=utf-8
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option
import datetime;
from content.models         import *;
from pageharvest.settings   import *;




    
class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-u', '--update',   dest='update_school', 
             help='update specified bbs parse config'),
        make_option( '-d', '--delete',   dest='delete_school', 
             help='clear specified bbs parse config'),
        make_option( '-a', '--add',   dest='add_school', 
             help='add specified bbs parse config'),
    )
    
    @staticmethod
    def update_schoolconfig( bn ):
        try:
            sbpc = SBPC.objects.get( bbsname = bn );
            c  = filter( lambda x: x['bbsname'] == bn , bbs_setting_list);
            if len(c)>0 : cc = c[0];
            sbpc.parseconfig = repr( cc );
            sbpc.chinesename = cc['chinesename']
            sbpc.save();
        except Exception,e:
            print e;
            return;
        print 'config updated successfully ', bn;

    def handle(self,  **options):
        if options.get('update_school'):
            bn = options.get('update_school');
            Command.update_schoolconfig( bn );
            
        if options.get('delete_school'):
            bn = options.get('delete_school');
            try:
                sbpc = SBPC.objects.get( bbsname = bn );
                sbpc.delete();
            except Exception,e:
                print e;
                return;
            print 'config delete successfully  ',bn;
        if options.get('add_school'):
            bn = options.get('add_school');
            try:
                c  = filter( lambda x: x['bbsname'] == bn , bbs_setting_list);
                bc = c[0];
                sbpc = SBPC( bbsname = bc['bbsname'], schoolname = bc['schoolname'],
                    rank = bc['rank'], chinesename = bc['chinesename'], 
                    parseconfig = bc );
                sbpc.save();
                sbpc.save();
            except Exception,e:
                print e;
                return;
            print 'config added successfully ',bn;
            
            

        
        
        
            

 
