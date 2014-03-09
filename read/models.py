import hashlib

from django.db import models
from django.db.models import FileField
from django.forms import forms, ModelForm
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from datetime import date

class BookFile(models.Model):
    orig_file = FileField( upload_to='pdf/%Y/%m',)
    sha1sum = models.CharField(max_length=47,primary_key=True)
    bookname = models.CharField(max_length=255, null=False )
    
    def save(self, *args, **kwargs):
            hasher = hashlib.sha1()
            for chunk in self.orig_file.chunks():
                hasher.update(chunk)
            new_sha1sum = hasher.hexdigest()
            try:
                obj = BookFile.objects.get( sha1sum = new_sha1sum )
            except ObjectDoesNotExist:
                self.sha1sum = new_sha1sum
                self.bookname = self.orig_file.name
                super(BookFile, self).save(*args, **kwargs)
                return self
            return obj
            
class BookForm(ModelForm):  
    class Meta:  
        model = BookFile 
        fields = ['orig_file']        
        
    def __init__(self, *args, **kwargs):
        FILE_KEY='files[]'
        uploaded_files = args[1]
        if uploaded_files.has_key( FILE_KEY ):
            uploaded_files['orig_file'] = uploaded_files[FILE_KEY] 
        
        super(BookForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(BookForm, self).clean()
        file = cleaned_data.get("orig_file")
        allowed_mime_type = ['application/pdf']
        max_upload_size = 50 * 1024 * 1024
        
        content_type = file.content_type
        if content_type not in allowed_mime_type:
            raise forms.ValidationError("file type not supported")
        if file._size > max_upload_size :
            raise forms.ValidationError("file too large: Actual[%d] limit[%d]"%(file._size,max_upload_size))
        return cleaned_data
        
    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(BookForm, self).save(commit=False)
        # do custom stuff
        if commit:
            return m.save()
        return m
        
        
class BookShelf(models.Model):
    sha1sum = models.CharField(max_length=47,primary_key=True)
    bookname = models.CharField(max_length=255 )
    user =  models.ForeignKey(User)
    
    def to_dict( self ):
        return {
            'bookname':self.bookname,
            'booksha1':self.sha1sum,
        }