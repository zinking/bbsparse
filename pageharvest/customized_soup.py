from BeautifulSoup import *

__author__ = "cenyongh@gmail.com"
__version__ = "0.1"
__license__ = "PSF"
class CustomizedSoup(BeautifulSoup):
    
    def __init__(self, *args, **kwargs):    
        self.ignore_tags = ['script','style']
        self.in_ignore_state = False
        BeautifulSoup.__init__(self, *args, **kwargs)
        
    def handle_comment(self, text):
        pass
    
    def unknown_starttag(self, name, attrs, selfClosing=0):
        if not self.in_ignore_state and not name in self.ignore_tags:
            BeautifulSoup.unknown_starttag(self, name, attrs, selfClosing)
        else:
            self.in_ignore_state = True
            
    def unknown_endtag(self, name):
        if name in self.ignore_tags:
            self.in_ignore_state = False
        else:
            BeautifulSoup.unknown_endtag(self, name)
            
    def handle_data(self, data):
        data = data.strip()
        if not self.in_ignore_state and len(data) != 0:
            BeautifulSoup.handle_data(self, data)