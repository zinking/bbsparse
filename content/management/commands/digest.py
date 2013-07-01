# -*- coding: utf-8 -*-
from datetime import *;
from settings import *;

from django.core.management.base import NoArgsCommand
from collections import defaultdict;
from operator import itemgetter
import jieba
import jieba.analyse

from content.models import *;
default_encoding='utf-8'
N=10
    
    
class Command(NoArgsCommand):
    help = "digout interesting things in the data"
    def handle_noargs(self, **options):
        try:
            self.parse_v2()
        except Exception,e:
            raise e;
    def parse_v1(self ):
        pcs = SBPC.objects.all().order_by('rank');
        asd = defaultdict(int)
        for p in pcs :  
            links = Link.objects.all().filter( school = p );
            sd = defaultdict(int)
            for link in links:
                ws = jieba.cut( link.title )
                for w in ws:
                    sd[w] += 1
            r = sorted(sd.items(), key=itemgetter(1), reverse=True)
            msg = ", ".join( [ "%s*%d"%( a[0], a[1]) for a in r[0:N] ] )
            print p.schoolname, msg
            for w in sd:
                asd[w]+=sd[w]
        r = sorted(sd.items(), key=itemgetter(1), reverse=True)
        msg = ", ".join( [ "%s*%d"%( a[0], a[1]) for a in r[0:N] ] )
        print 'TOTAL', msg 
        
    def parse_v2(self ):
        pcs = SBPC.objects.all().order_by('rank');
        c = u"";
        for p in pcs :  
            links = Link.objects.all().filter( school = p );
            cc = u"";
            for link in links:
                cc += link.title
            tt = jieba.analyse.extract_tags(cc, topK=N)
            #msg = ", ".join( [ "%s*%.2f"%( a[1], a[0]) for a in tt ] )
            msg = " ".join( [ "%s "%( a[1]) for a in tt ] )
            print p.schoolname, msg
            print "\n"
            c += cc
        tt = jieba.analyse.extract_tags(c, topK=N)
        msg = ", ".join( [ "%s * %.2f"%( a[1], a[0]) for a in tt ] )
        print "TOTAL", msg


