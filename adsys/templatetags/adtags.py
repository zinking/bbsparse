from django import template
import  django.template.defaultfilters as defaultfilters
register = template.Library()
import logging;
from adsys.models import *;
from ragendja.dbutils import *;

@register.filter("adcontent")
def adcontent( mark = None):
    """
    insert specified ad content into template
    """
    from adsys.settings import AD_PROMOTION;
    if ( AD_PROMOTION ): return "";
    try:
        c = get_object( AdSetting , "aid =", 1);
    except Exception,e:
        logging.error('Config AdSetting does not exist:%e');
        return "";
    if ( mark == 'admap' ):
        return c.bmap;
    elif ( mark == 'admapxn' ):
        return c.smap;
        