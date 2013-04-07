# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from datetime import *;
import time;
import random;
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.shortcuts import render_to_response as rtr;

from google.appengine.ext import db
from google.appengine.api import users
from content.decorators import *;

from models import *;
import logging;


import urllib2,time;
def getImgData( url ):
    try: 
        imgdata = urllib2.urlopen( url ).read();
    except Exception, e: 
        error_msg = "Failed to open following img url %s" % (url);
        logging.error( error_msg );
        raise Exception(error_msg);
    return imgdata;



#@admin_user_only
def ad_table_op( request,  template='default.html', extra_context=None):
    context = RequestContext(request);
    if ( 'op' in request.GET  ):
        op = request.GET['op'];
    if ( 'nm' in request.GET  ):
        bn = request.GET['nm'];
        
    if op == 'setup':
        c = repr( { 'url':'http://hdn.xnimg.cn/photos/hdn311/20090723/1125/tiny_nI6Y_12349e204237.jpg'} );
        db_create( LuckyList,  config = c, xid="224298828" );
        db_create( LuckyList,  config = c, xid="228993921" );
        db_create( LuckyList,  config = c, xid="264994936" );
        db_create( LuckyList,  config = c, xid="30749403" );
        db_create( LuckyList,  config = c, xid="222534363" );
        db_create( LuckyList,  config = c, xid="329844096" );
        db_create( LuckyList,  config = c, xid="24020291" );
        db_create( LuckyList,  config = c, xid="223164709" );
    if op == 'setimg':
        flag = True;
        try:
            c = get_object( AdSetting , "aid =", 1);
        except Exception,e:
            flag = False;
        if( not flag ): c.delete();
        cc = {
            'b':'http://super-museum.appspot.com/media/adgrid.jpg',
            's':'http://super-museum.appspot.com/media/adgridxn.jpg',
        }
        bi = getImgData( cc['b'] );
        si = getImgData( cc['s'] );
        db_create( AdSetting,  config = repr(cc), bsrc=bi , ssrc=si );
    msg =  'Admin setup adsystem data successfully';
    context['msg'] = msg;
    logging.info( msg );

    return rtr( template, context, context_instance=extra_context)
    
QUOTA = 27 * 1000;
def cron_avtars( request,  template='default.html', extra_context=None):    
    context = RequestContext(request);
    ll = get_object_list( LuckyList, 'mark =', False );
    total_cost = 0;i=0;
    for i,l in enumerate(ll):
        if total_cost >= QUOTA: break;
        t1 = time.time();
        c = eval(l.config);
        try:
            l.avatar = getImgData( c['url'] );
        except Exception,e:
            logging.debug('Lucky ID avatar cron failed %s'%(e));
            continue;
        l.mark = True;
        l.put();
        t2 = time.time();
        total_cost += t2-t1;
    msg = 'Totally %d LUCKY IDS getCroned and Erolled in DB within %d ms'%(i,total_cost);
    context['msg'] = msg;
    return rtr( template, context, context_instance=extra_context)
    
def cron_composer( request,  template='default.html', extra_context=None):
    from ad import adop;
    context = RequestContext(request);
    try:
        c = get_object( AdSetting , "aid =", 1);
    except Exception,e:
        logging.error('Config AdSetting does not exist');
        return;
    bc,sc = generate_ad_config();
    br = adop.generate_img_from_setting(bc);
    sr = adop.generate_img_from_setting(sc);
    #this will be ugly done because I don't want to modify the bunch code of generate....
    bc['gridxn'] = sc['grid'];
    bc['current_ad_list_xn'] = sc['current_ad_list'];
    bm,sm = adop.generate_linkmap(bc);#notice this function has dependency on the uptwo calls;
    c.bres = br;c.sres = sr;c.bmap = db.Text(bm, encoding='utf-8'); c.smap = db.Text(sm, encoding='utf-8');
    c.put();
    msg = 'Successfully composed';
    context['msg'] = msg;
    return rtr( template, context, context_instance=extra_context)
    
def view_avtars( request,  template='default.html', extra_context=None):
    context = RequestContext(request);
    if ( 'id' in request.GET ):
        id = request.GET['id'];
    else :
        id = "264994936";
    from adsys.settings import MEDIA_URL,AD_PROMOTION;

    default_grid_img = MEDIA_URL + 'content/images/adgrid.jpg';
    default_grid_imgxn = MEDIA_URL + 'content/images/adgridxn.jpg';
    

    if ( id == 'adgrid' or id == 'adgridxn' ):
        if ( AD_PROMOTION ):
            if ( id == 'adgrid' ):
                return HttpResponseRedirect(default_grid_img);
            elif ( id == 'adgridxn' ):
                return HttpResponseRedirect(default_grid_imgxn);
        else:
            try:
                c = get_object( AdSetting , "aid =", 1);
                if ( id == 'adgrid' ):
                    return HttpResponse(c.bres, mimetype="image/jpg");
                elif ( id == 'adgridxn' ):
                    return HttpResponse(c.sres, mimetype="image/jpg");
            except Exception,e:
                logging.debug(e);
                if ( id == 'adgrid' ):
                    return HttpResponseRedirect(default_grid_img);
                elif ( id == 'adgridxn' ):
                    return HttpResponseRedirect(default_grid_imgxn);

    try:
        item = get_object(LuckyList, 'xid =' , id);
        return HttpResponse(item.avatar, mimetype="image/jpg");
    except Exception,e:
        logging.debug(e);
    context['msg'] = 'Invalid File id Passed' ; 
    return rtr( template, context, context_instance=extra_context)

    
    

    
def generate_ad_config():
    c = {"row": 3, "adgridsize": 30, "addcolxn": 23, 'addcol':31 };
    iii = {
    "title": "LQQ", 
    "link": "http://www.renren.com/profile.do?id=36783992", 
    "location": ["E1", "E1"], 
    "buyer": "me", 
    "alt": "LQQ", 
    "createtime": "datetime.datetime(2010, 3, 20, 22, 36, 27, 384000)", 
    "id": "F:\\WorkSpace\\BBS_PARSE_V2\\AD\\pimages\\lqq.jpg"}
    
    col = [ chr( ord('A')+j) for j in range(0,26) ];
    for i in [ chr( ord('0')+j) for j in range(0,4) ] : col.append(i);
    col_xn = [ chr( ord('A')+j) for j in range(0,23) ];
    row = [ chr( ord('1')+j) for j in range(0,3) ];
    all_coords  = []; allxn_coords = [];
    for i in row:
        for j in col:
            all_coords.append( j+i );
    for i in row:
        for j in col_xn:
            allxn_coords.append( j+i );
            
    q = LuckyList.all(); qc = q.count();
    try:
        aconfig = get_object( AdSetting, "aid =", 1 );
    except Exception,e:
        logging.debug( "failed to get Adsetting during setup exit" );
        return;
    import random;
    count = random.randint(0,qc );
    qc = min( 20, qc );
    q.fetch(qc);
    #generate big image configs
    bc = c.copy();
    bc['file'] = aconfig.bsrc;
    coords = random.sample( all_coords, qc );
    current_ad_list = [];
    for i in range(1,qc):
        item = iii.copy();
        item['id'] = q[i].xid;
        item['location'] = [ coords[i], coords[i] ];
        item['data'] = q[i].avatar;
        current_ad_list.append( item );
    bc['current_ad_list'] = current_ad_list;
    bc['grid'] = [ [ None for i in range(0,c['addcol']) ]  for j in range(0,c['row']) ]
    #generate small image configs
    sc = c.copy();
    sc['file'] = aconfig.ssrc;
    coords = random.sample( allxn_coords, qc );
    current_ad_list = [];
    for i in range(1,qc):
        item = iii.copy();
        item['id'] = q[i].xid;
        item['location'] = [ coords[i], coords[i] ];
        item['data'] = q[i].avatar;
        current_ad_list.append( item );
    sc['current_ad_list'] = current_ad_list;
    sc['grid'] = [ [ None for i in range(0,c['addcolxn']) ]  for j in range(0,c['row']) ]
    
    return bc,sc;
    
    
    
            

