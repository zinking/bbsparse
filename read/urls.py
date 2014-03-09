# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView

from read.views import *


urlpatterns = patterns('',
    url(r'^$$',         reader_home ,{'template':'read.html'},   name='home'),
    url(r'^upload_pdf_file/$',   upload_file , {} ,   name='uploadfile'),
    url(r'^download_file/(?P<pdfname>\b[0-9a-f]{5,40}).pdf$',      download_file , {} ,   name='downloadfile'),
    url(r'^read_book$',          read_book , {'template':'viewer.html'} ,   name='readbook'),
    url(r'^booksubs.json/$',     list_book_subscription , {} ,   name='listpdf'),
)

