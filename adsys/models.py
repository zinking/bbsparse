# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from google.appengine.ext import db


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

class AdSetting(db.Model):
    aid         = db.IntegerProperty(   default = 1  );
    config      = db.StringProperty( multiline=True , default="" );
    bsrc        = db.BlobProperty();
    ssrc        = db.BlobProperty();
    bres        = db.BlobProperty();
    sres        = db.BlobProperty();
    bmap        = db.TextProperty();
    smap        = db.TextProperty();
    
    
class LuckyList(db.Model):
    xid         = db.StringProperty(   default = ""  );
    avatar      = db.BlobProperty();
    config      = db.StringProperty( multiline=True , default="" );
    mark        = db.BooleanProperty( default = False );#indicating if it hasbeen croned


