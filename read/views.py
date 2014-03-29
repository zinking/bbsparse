# Create your views here.
import os
import logging
from django.http import *
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.static import serve
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist

from settings import FILE_ROOT
from read.models import *
logger = logging.getLogger('bbs_dig')

@login_required
@ensure_csrf_cookie
def reader_home(request, template ):
    context = RequestContext(request)
    return render_to_response( template, context, RequestContext(request))
    
@login_required
def list_book_subscription(request ):
    booksubs = BookShelf.objects.filter( user = request.user );
    result = map( lambda x:x.to_dict(), booksubs );
    data = simplejson.dumps( result)
    return HttpResponse(data, mimetype="application/json")
    

@login_required
@cache_page(60 * 60 * 24 * 7 ) # cache a week
def download_file(request, pdfname):
    file_sha1sum = pdfname
    try:
        obj = BookFile.objects.get( sha1sum = file_sha1sum )
        return serve(request, os.path.basename(obj.orig_file.path), os.path.dirname(obj.orig_file.path))
    except ObjectDoesNotExist:
        return HttpResponseNotFound('Page not found')
    except Exception,e:
        logger.info( 'serving file error %s'%(e) );
    return HttpResponseNotFound('Page not found')
            
@login_required
def read_book(request, template ):
    context = RequestContext(request)
    if 'booksha1' in request.GET:
        booksha1 = request.GET['booksha1']
        try:
            obj = BookFile.objects.get( sha1sum = booksha1 )
            context['booksha1'] = booksha1
            context['bookname'] = obj.bookname
            return render_to_response( template, context, RequestContext(request))
        except ObjectDoesNotExist:
            pass
        

    return HttpResponseNotFound('Page not found')
       
    
    
@login_required
def upload_file(request):
    result = {
        'success':False,
    }
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        
        if form.is_valid():
            result['success'] = True
            pdf = form.save()
            current_book_name = request.FILES['orig_file'].name
            #current_book_name = form.fields['orig_file']
            #people might upload same file with different name
            #this is to make them subs use their book name
            user_sub = BookShelf( sha1sum = pdf.sha1sum, user = request.user, bookname = current_book_name  )
            user_sub.save();
            logger.info( '%s subscribed book %s' % ( request.user.username, current_book_name ) )
            result['msg'] = 'file uploaded' 
            logger.info( '1 file uploaded' )
        else:
            error_msg =  form.errors.items()
            logger.info( error_msg );
            result['msg'] = error_msg 
    else:
        result = 0;
    data = simplejson.dumps( result )
    return HttpResponse(data, mimetype="application/json")

    
 