# -*- coding: utf-8 -*-

import time;
import random;
from datetime import *;
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson


from django.core  import serializers
from django.shortcuts import render_to_response as rtr;
#from content.utils import render_to_response as rtrg;

from django.views.decorators.cache import cache_page


from pageharvest.settings  import *;
from pageharvest.bbsparser import *;
from settings import *;

from models import *;

#from adsys.decorators import random_record_xn_access;
@cache_page(60 * 15) #15 minutes
def viewbyschool(request, template='content_by_school.html', extra_context=None):
    context = RequestContext(request); 
    sbpclist = SBPC.objects.filter( status = STATUS_NORMAL ).order_by( 'rank' );
    bbstop10infolist = [];
    for sbpc in sbpclist:
        top10list = Link.objects.filter( school = sbpc ).order_by('-updatetime')[0:10];
        
        bbstop10infolist.append( {'sbpc': jsbpc,'itemlist': jtop10list,} );
    
    length = len( bbstop10infolist );
    context['col1'] = bbstop10infolist[0:length/2];
    context['col2'] = bbstop10infolist[length/2:length ];
    recommendlist = Link.objects.filter( tags = 'recommend' ).order_by('-updatetime')[0:10];
    context['recommend'] = recommendlist;
    context['announcement'] = OptionSet.getValue('announcement', 'Currently No Announcement');
    context_instance=RequestContext(request)
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);
    
@cache_page(60 * 15)
def linkbyschools(request, template='content_by_school.html', extra_context=None):
    sbpclist = SBPC.objects.filter( status = STATUS_NORMAL ).order_by( 'rank' );
    bbstop10infolist = [];
    result = {}
    for sbpc in sbpclist:
        top10list = Link.objects.filter( school = sbpc ).order_by('-updatetime')[0:10];
        d_top10list = map( lambda x:x.to_dict(), top10list );
        bbstop10infolist.append( {'sbpc': sbpc.to_dict(),'itemlist': d_top10list,} );
    
    length = len( bbstop10infolist );
    result['col1'] = bbstop10infolist[0:length/2];
    result['col2'] = bbstop10infolist[length/2:length ];
    data = simplejson.dumps( result)
    return HttpResponse(data, mimetype="application/json")
    
    
@cache_page(60 * 30)    
def view_parsing_status(request, template='status.html', extra_context=None):
    context = RequestContext(request); 
    sbpclist = SBPC.objects.all().order_by( 'rank' );
    status_dsc = [ 'danger', 'success', 'danger', 'warning'];
    success_count = 0
    for pc in sbpclist:
        pc.statusinfo = status_dsc[ pc.status ];
        pc.parseconfig = eval( pc.parseconfig );
        success_count += 1 if pc.statusinfo=='success' else 0
    context['schools'] = sbpclist;
    context['count'] = len(sbpclist);
    context['progress'] = (float)(success_count) / (float)(len(sbpclist)) * 100
    context_instance=RequestContext(request);
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);
    
@cache_page(60 * 45)
def viewframedcontentV2(request, template='framed_link_content.html', extra_context=None):
    context = RequestContext(request);
    linkid = request.GET.get('l', '0');

    try:
        linkitem = Link.objects.get( id = int(linkid) );
        linkitem.visitcount = linkitem.visitcount + 1;
        linkitem.save();
    except Link.DoesNotExist:
        info = "Exception when get link using id:%s, %s"%(linkid,e);
        raise Http404;
    except Exception,e:
        pass;
    context['link'] = linkitem;
    context_instance=RequestContext(request);
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);

    
    

def gae_cron_job_sendblog( request , template='cron_mblog_result.html',extra_context=None):
    context=RequestContext(request);
    #now         = datetime.now()
    delta       = timedelta( hours = -4 );
    criteria    = datetime.datetime.now() + delta;

    hourlylinks = get_object_list( Link, 'createtime > ', criteria ).order('-createtime').order('-visitcount');
    recommend_count = 0;
    sina_list = [];n163_list = [];twitter_list=[];
    
    bhandle = Microblog();
    for links in hourlylinks:
        if( not bhandle.skip_sina and not links.contain_tag( SINA_MBLOG ) ): 
            sina_list.append( links );
            links.tags.append( SINA_MBLOG );
            recommend_count += 1;
        if( not bhandle.skip_n163 and not links.contain_tag( N163_MBLOG ) ): 
            n163_list.append( links );
            links.tags.append( N163_MBLOG );
            recommend_count += 1;
        if( not bhandle.skip_twitter and not links.contain_tag( TWITTER_MBLOG ) ): 
            twitter_list.append( links );
            links.tags.append( TWITTER_MBLOG );
            recommend_count += 1;
        links.put();
        if( recommend_count > bhandle.quota ):break;
    
    
    for links in sina_list:
        bhandle.post_sina_msg( links.get_mblog_str() );
    for links in n163_list:
        bhandle.post_n163_msg( links.get_mblog_str() );
    for links in twitter_list:
        bhandle.post_twitter_msg( links.get_mblog_item() );
  
    context['sina_count']    = len( sina_list );
    context['n163_count']    = len( n163_list );
    context['twitter_count']    = len( twitter_list );
    context_instance=RequestContext(request);
    return render_to_response(template, context,context_instance);



