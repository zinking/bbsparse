# -*- coding: utf-8 -*-
from functools import wraps;

from ragendja.dbutils import *;

from pyxn import *;
from settings import *;

from adsys.models import *;
from adsys.views  import getImgData;
import logging;


xn = Xiaonei(api_key=XIAONEI_API_KEY, secret_key=XIAONEI_SECRET_KEY, 
        app_name=XIAONEI_APP_NAME, callback_path=XIAONEI_CALLBACK_PATH, internal=XIAONEI_INTERNAL)



def random_record_xn_access(view):
    """
    Decorator that random record xn access infomation and store them
    """
    def wrapped(request, *args, **kwargs):
        if not xn.check_session(request): 
            logging.debug('!!! Not Request from XiaoNei, Neglected');
            return view(request, *args, **kwargs);
        id = xn.uid;
        randomly_delete_accessinfo();
        try:
            ll = get_object( LuckyList, 'xid =', id );
        except Exception,e:
            req = xn.users.getInfo(uids=[xn.uid],fields=["name","birthday","tinyurl"]);
            cc = req[0]; adata = getImgData( cc['tinyurl'] );
            ll = db_create( LuckyList, xid=id, config=cc, avatar=adata );
            logging.debug('!!! XiaoNei User Infomation Successfully recorded');
        return view(request, *args, **kwargs);
    return wraps(view)(wrapped)
    
def randomly_delete_accessinfo():
    qa = LuckyList.all();
    tc = qa.count();
    if (tc<=30): return;
    import random;
    index = random.randint(0,tc);
    qa[index].delete();
    

        