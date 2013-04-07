# coding=utf-8
"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``RegistrationProfile.objects.delete_expired_users()``, which
contains the actual logic for determining which accounts are deleted.

Advertisement Management Utils for BBSTOP 10 SITE

"""
"""
Advertisement settings and data file specification 
'add grid size'    : 30px
'add row col'      : 31
'xn add row col'   : 23
'row'              : 3
'current ad list'  : 
    #ad item specification
    title    :    ''
    alt      :    '' # if not specified, the same as title
    location :    ['A1','A1'] # location on ad grid
    link     :    ''
    createtime:   ''
    buyer    :    ''
"""

from django.core.management.base import BaseCommand
from optparse import make_option
from django.utils import simplejson

import datetime;
import time;
import os;

CWD = os.getcwd()+"\\";
AD_GRID_FILE    = CWD + 'AD\\images\\adgrid.jpg';
AD_GRID_FILE_XN = CWD + 'AD\\images\\adgridxn.jpg';
RESULT_AD       = CWD + 'AD\\adgrid.jpg';
RESULT_AD_XN    = CWD + 'AD\\adgridxn.jpg';

MAPFILE         = CWD + 'AD\\admap.html';
XNMAPFILE       = CWD + 'AD\\xn_admap.html';

SETTING_FILE    = CWD + 'Ad\\record.json';
VALID_PERIOD    = datetime.timedelta( days = 7 );
#SETTING         = {};

import Image,ImageDraw,ImageFont; 
class AdOperator(object):
    def __init__(self): 
        self.dm={};     
        self.md={};
        for i in range( ord('A'), ord('Z')+1 ):
            self.dm[chr(i)] = i - ord('A');
            self.md[ i-ord('A') ] = chr(i);
        for i in range( ord('0'), ord('8')+1 ):
            self.dm[chr(i)] = i - ord('0') + 26;
            self.md[ i - ord('0') + 26 ] = chr(i);

    def transform_coordinate(self,coordinate,setting,adconfig):
        #print 'x', self.dm[ s[0] ];
        #print 'y', int(s[1])-1;
        m = self.dm;
        gs = setting['adgridsize'];
        L = coordinate[0];
        R = coordinate[1];
        upleft = m[L[0]]; uptop = (int(L[1])-1); downright = (m[R[0]]+1); downbottom = (int(R[1])); 
        coord =  ( upleft*gs, uptop*gs, downright*gs, downbottom*gs );
        size  =  ((  downright - upleft )*gs, ( downbottom - uptop  )*gs );
        adconfig['coord'] = "%s,%s,%s,%s"%(coord[0],coord[1],coord[2],coord[3]);
        for j in range( upleft, downright):
            for i in range( uptop, downbottom ):
                setting['grid'][i][j] = adconfig;
                setting['xngrid'][i][j] = adconfig;

        return ( coord , size );
    def generate_img_from_setting(self, setting):
        oad     = Image.open(AD_GRID_FILE);
        oadxn   = Image.open(AD_GRID_FILE_XN);
        
        for adconfig in setting['current_ad_list']:
            ad_img = Image.open( adconfig['gridsrc']);
            ( coord , size ) = self.transform_coordinate( adconfig['location'] , setting, adconfig );
            print coord;
            print size;
            #ad_img.thumbnail( size, Image.ANTIALIAS); 
            ad_img = ad_img.resize(size);
            #ad_img.show();
            oad.paste( ad_img, coord );
            oadxn.paste( ad_img, coord );

        oad.save(RESULT_AD);
        oadxn.save(RESULT_AD_XN);
        
    def draw_smallgrid( self, draw, txt, coord ):
        def randcolor():
            import random;
            return ( random.randrange(0,255),random.randrange(0,255),random.randrange(0,255));
        (x,y,z,w) = coord;
        linewidth = 2;
        #linecolor = "#CECECE";
        linecolor = randcolor();
        fontcolor = randcolor();
        draw.line( (x,y,z,y) ,fill=linecolor, width = linewidth);
        draw.line( (x,y,x,w) ,fill=linecolor, width = linewidth);
        draw.line( (z,y,z,w) ,fill=linecolor, width = linewidth);
        draw.line( (x,w,z,w) ,fill=linecolor, width = linewidth);
        #font = ImageFont.truetype("msyh.ttf", 20);
        #print fontcolor
        font = ImageFont.truetype("YaHei.Consolas.1.11.ttf", 20);
        draw.text((x+4, y+0), txt, font=font, fill=fontcolor);
    
    def get_char(self, i,j):
            return self.md[j]+str(i+1);
        
    def generate_original_img(self,setting):
        def get_coord( j, i, gs ):
            return (i*gs,j*gs, (i+1)*gs, (j+1)*gs );
            
        gs = setting['adgridsize'];
        adsize   = ( setting['addcol'] * setting['adgridsize'] , setting['row'] * gs+1 )
        xnadsize = ( setting['xnaddcol'] * setting['adgridsize'] , setting['row'] * gs+1 )
        admap = Image.new('RGB', adsize , "#FFF" );
        addraw = ImageDraw.Draw(admap);
        xnadmap = Image.new('RGB', xnadsize , "#FFF" );
        xnaddraw = ImageDraw.Draw(xnadmap);
#PIL DRAW MODUAL OPTION REFERECE http://www.numenta.com/for-developers/software/pydoc/PIL.ImageDraw.html
        for i in range(0, setting['row'] ):
            for j in range( 0, setting['addcol'] ):
                coord = get_coord(i,j,setting['adgridsize']);
                self.draw_smallgrid( addraw, self.get_char(i,j), get_coord(i,j,gs) );
        for i in range(0, setting['row'] ):
            for j in range( 0, setting['xnaddcol'] ):
                coord = get_coord(i,j,setting['adgridsize']);
                self.draw_smallgrid( xnaddraw, self.get_char(i,j), get_coord(i,j,gs) );
        del addraw;
        del xnaddraw;
        admap.save(AD_GRID_FILE);
        xnadmap.save(AD_GRID_FILE_XN);


        
    

    def generate_linkmap(self,setting):
        def get_coord_render( j, i, gs ):
            return "%s,%s,%s,%s"%(i*gs,j*gs, (i+1)*gs, (j+1)*gs );
            
        
        NoneAddPattern = u"""<area shape="rect" coords="%ls" target="_blank" title="广告位招租"
                    	href="http://item.taobao.com/auction/item_detail.htm?item_num_id=4668559225" alt="广告位招" />"""
        AddPattern = u"""<area shape="rect" coords="%ls" target="_blank" title="%ls" href="%ls" alt="%ls" />"""
        contentmap = "";
        count = 0;
        for i in range(0, setting['row'] ):
            for j in range( 0, setting['addcol'] ):
                if( setting['grid'][i][j] == None ):
                    contentmap += NoneAddPattern%(get_coord_render(i,j,setting['adgridsize'])) +'\n';
                # else:
                    # c = setting['grid'][i][j];
                    # contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        for c in setting['current_ad_list']:
            contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        grid_map = """<map name="AV-eggs">\n%s\n</map>""" %(contentmap);
        f = open(MAPFILE, 'wb')
        grid_map = unicode.encode(grid_map, 'utf-8')
        f.write(grid_map + "\n")
        f.close();
        contentmap = "";
        for i in range(0, setting['row'] ):
            for j in range( 0, setting['xnaddcol'] ):
                if( setting['xngrid'][i][j] == None ):
                    contentmap += NoneAddPattern%(get_coord_render(i,j,setting['adgridsize'])) +'\n';
                # else:
                    # print i,j, 'l occupied'
                    # contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        for c in setting['current_ad_list']:
            contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        print count;
        grid_map = """<map name="AV-eggs">\n%s\n</map>""" %(contentmap);
        f = open(XNMAPFILE, 'wb')
        grid_map = unicode.encode(grid_map, 'utf-8')
        f.write(grid_map + "\n")
        f.close();
                    
        
op = AdOperator();

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-l', '--listad',  dest='listad', 
             help='list currently occupied adds'),
        make_option( '-a', '--addad',   dest='addad', 
             help='add adds to current board'),
        make_option( '-d', '--deletead',  dest='deletead', 
             help='delete specified ad'),
        make_option( '-g', '--generate',  dest='generate', 
             help='generate add specification file'),
        make_option( '-n', '--newgridimg',  dest='new', 
             help='generate new  grid file'),
    )

    def handle(self,  **options):
        def read_setting():
            f = open(SETTING_FILE, 'r+');
            setting = simplejson.load( f );
            for item in setting['current_ad_list']:
                 item['createtime'] = eval( item['createtime'] );
            #print setting;
            print 'Read setting from record file';
            f.close();
            #this fucking reference copy just made me mad on saturday night
            #setting['grid']     = [ [None]*setting['addcol'] ] * setting['row'];
            #setting['xngrid']   = [ [None]*setting['xnaddcol'] ] * setting['row'];
            setting['grid'] = [ [ None for i in range(0,setting['addcol']) ]  for j in range(0,setting['row']) ]
            setting['xngrid'] = [ [ None for i in range(0,setting['addcol']) ]  for j in range(0,setting['row']) ]
            return setting;
        
        def write_setting( setting ):
            s = simplejson.dumps(setting)
            #print s;
            f = open(SETTING_FILE, 'w')
            f.write(s + "\n")
            f.close();
            print 'write setting into record file';
            
            
        
        def isvalidad( ad ):
            if ad['createtime'] + VALID_PERIOD > datetime.datetime.now(): return 'valid'
            else: return 'Invalid';
        #util functions
        
        if options.get('listad'):
            setting = read_setting();
            for aditem in setting['current_ad_list']:
                print "Ad item: buyer: %8s, title: %8s ,location: %8s, alt: %8s, status: %s"\
                    %( aditem['buyer'],aditem['title'],str(aditem['location']),str(aditem['alt']), isvalidad(aditem));
            #global SETTING
            #print SETTING;
        
        if options.get('new'):
            setting = read_setting();
            op.generate_original_img(setting);
            print 'new image successfully generated';

        if options.get('addad'):
            setting = read_setting();
            op.generate_img_from_setting( setting);
            op.generate_linkmap(setting);
            print 'new config file successfully generated';
            
        if options.get('generate'):
            setting = {};
            setting['adgridsize'] = 30;
            setting['addcol'] = 31;
            setting['xnaddcol'] = 23;
            setting['row'] = 3;
            sampleitem = {};
            sampleitem['title'] = 'sample title';
            sampleitem['alt']   = 'alt';
            sampleitem['location'] = ['A1','B1'];
            sampleitem['link'] = 'sample link';
            sampleitem['buyer'] = 'buyer';
            sampleitem['gridsrc'] = CWD + 'AD\\pimages\\'+'gridsrc.jpg';
            sampleitem['createtime'] = repr( datetime.datetime.now() );
            setting['current_ad_list'] = [sampleitem];          
            write_setting(setting);

        