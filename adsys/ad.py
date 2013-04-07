# coding=utf-8


import datetime;
import time;



from google.appengine.api import images; 
from google.appengine.api.images import Image;
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

        return ( coord , size );
        
    def generate_img_from_setting(self, setting):
        oad     = Image(setting['file']);
        otup = ( oad, 0, 0, 1.0, images.TOP_LEFT );
        cplist  = [ otup ];
        for adconfig in setting['current_ad_list']:
            ad_img =  adconfig['data'];
            ( coord , size ) = self.transform_coordinate( adconfig['location'] , setting, adconfig );
            ad_img = images.resize( ad_img, size[0], size[1] );
            itup = ( ad_img, coord[0]+1, coord[1]+2, 1.0, images.TOP_LEFT );
            cplist.append( itup );
        return  images.composite( cplist , oad.width, oad.height,0,images.JPEG); 
    
    def get_char(self, i,j):
            return self.md[j]+str(i+1);

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
        for c in setting['current_ad_list']:
            contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        grid_map = """<map name="AV-eggs">\n%s\n</map>""" %(contentmap);
        grid_map = unicode.encode(grid_map, 'utf-8')
        bmap = grid_map;
        contentmap = "";
        for i in range(0, setting['row'] ):
            for j in range( 0, setting['addcolxn'] ):
                if( setting['gridxn'][i][j] == None ):
                    contentmap += NoneAddPattern%(get_coord_render(i,j,setting['adgridsize'])) +'\n';
                # else:
                    # print i,j, 'l occupied'
                    # contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        for c in setting['current_ad_list_xn']:
            contentmap += AddPattern%( c['coord'], c['title'], c['link'], c['alt'] ) +'\n';
        grid_map = """<map name="AV-eggs">\n%s\n</map>""" %(contentmap);
        grid_map = unicode.encode(grid_map, 'utf-8')
        smap = grid_map;
        return bmap,smap;
                    
adop = AdOperator();


        