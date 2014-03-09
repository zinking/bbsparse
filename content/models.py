# -*- coding: utf-8 -*-
from django.db import models
from django.utils import simplejson
from django.core  import serializers



STATUS_NORMAL = 1;
STATUS_UNREACHABLE = 2;
STATUS_EXCEPTION = 3;

class QuerySetEncoder( simplejson.JSONEncoder ):
    """
    Encoding QuerySet into JSON format.
    """
    def default( self, object ):
        try:
            return serializers.serialize( "json", object,
                                          ensure_ascii = False )
        except:
            return simplejson.JSONEncoder.default( self, object )

class SBPC(models.Model):#SCHOOL BBS PARSE CONFIG
    bbsname         = models.CharField( max_length=75 ,default = "" );
    schoolname      = models.CharField( max_length=75 ,default = "" );
    chinesename     = models.CharField( max_length=75 ,default = "" );
    rank            = models.IntegerField( default = 0 );
    lastfresh       = models.DateTimeField( null=True );
    totalparse      = models.IntegerField( default = 0 );
    failedparse     = models.IntegerField( default = 0 );
    totalparsetime  = models.FloatField( default = 0 );
    status          = models.IntegerField( default = 1 );
    parseconfig     = models.TextField( null=True );
    
    def to_dict( self ):
        return {
            'bbsname':self.bbsname,
            'schoolname':self.schoolname,
            'chinesename':self.chinesename,
        }
 
class Link(models.Model):
    
    board           = models.CharField( max_length=15  ,default = "" );
    title           = models.CharField( max_length=750 ,default = "" );
    titlelink       = models.CharField( max_length=750 ,default = "" );
    author          = models.CharField( max_length=75  ,default = "" );
    visitcount      = models.IntegerField( default = 1 );
    postcount       = models.IntegerField( default = 1 );
    school          = models.ForeignKey(SBPC);
    createtime      = models.DateTimeField( null=False );
    updatetime      = models.DateTimeField( null=False );
    pagecache       = models.TextField( null=True );
    tags            = models.TextField( null=True );
#    tags            = ListField( models.CharField(max_length=75), null=True );
    
    def get_mblog_str(self):
        from django.core.urlresolvers import reverse;
        link_pattern =  ROOT_URL + reverse('content_framed_detail') + '?linkid=%s';
        msg = "[%s] %s %s" %(self.school.chinesename, self.title, link_pattern %(self.id) );
        if self.author != "": msg+= " BY "+self.author;
        return msg;
        
    def to_dict( self ):
        return {
            'board':self.board,
            'title':self.title,
            'titlelink':self.titlelink,
        }

        
class OptionSet(models.Model):
	name    = models.CharField( max_length=750 );
	value   = models.TextField( null=False );

	@classmethod
	def getValue(cls,name,default=None):
		try:
			opt=OptionSet.get_by_key_name(name)
			return pickle.loads(str(opt.value))
		except:
			return default

	@classmethod
	def setValue(cls,name,value):
		opt=OptionSet.get_or_insert(name)
		opt.name=name
		opt.value=pickle.dumps(value)
		opt.put()

	@classmethod
	def remove(cls,name):
		opt= OptionSet.get_by_key_name(name)
		if opt:
			opt.delete()
    