from BeautifulSoup import *
import re
from customized_soup import CustomizedSoup

'''
Assume the Page Being extract looks like this,

content = "
<html>
    <body>
        <div id='xx'>
             <table>
                 <tr>
                       <td>Title</td>
                       <td>xxxxxxxxxxx</td>
                 </tr>
                 <tr>
                       <td>Date</td>
                       <td>yyyyyyyyyyy</td>
                 </tr>
                 <tr>
                       <td>Tags</td>
                       <td>zzzzzzzzzzzz</td>
                 </tr>
             </table>
        </div>
    </body>
</html>
"


Example 1: To extract title, date ,tags from the page.What you need to do is:


 pattern = "
<div>
   <table>
       <tr>
           <td>*</td>
           <td>$title</td>
       </tr>
       <tr>
           <td>*</td>
           <td>$date</td>
       </tr>
       <tr>
           <td>*</td>
           <td>$content</td>
       </tr>
   </table>
</div>
"

doc = CustomizedSoup(index_page)
scraper = Scraper(pattern)
ret = scraper.match(doc)            #    this will return all the tags match the pattern
values = scraper.extract(ret[0])    #    get the value that define as '$xx'

#values is a dict, according to the previous example and pattern, it will look like this
{'title':'xxxxxxx','date':'yyyyyyy','content':'zzzzzzzzz'}

Example 2: just extract the title
pattern = "
<div>
   <table>
       <tr>
           <td>*</td>
           <td>$title</td>
       </tr>
        *                            #    use asterisk to match all the content that you don't care
   </table>
</div>
"

doc = CustomizedSoup(index_page)
scraper = Scraper(pattern)
ret = scraper.match(doc)    
values = scraper.extract(ret[0])

#values is a dict, according to the previous example and pattern, it will look like this
{'title':'xxxxxxx'}


Example 3: extract the <table> tag as a whole
pattern = "
<div>
   *$content
</div>
"

doc = CustomizedSoup(index_page)
scraper = Scraper(pattern)
ret = scraper.match(doc)    
values = scraper.extract(ret[0])

#values is a dict, according to the previous example and pattern, it will look like this
{'content':[<table><tr>...</tr></table>]}

More example can be find in the scraper_test.py

'''

__author__ = "cenyongh@gmail.com"
__version__ = "0.1"
__license__ = "PSF"

class Scraper(object):
    def __init__(self, pattern):
        self.pattern = CustomizedSoup(pattern).contents[0]
    
    def match(self, root):
        candidates = root.findAll(self.pattern.name)
        ret = [candidate for candidate in candidates if self.matchByType(self.pattern, candidate)]
        return ret            

    def matchByType(self, exp, actual):        
        if type(exp) != type(actual):
            return False
        elif isinstance(exp, Tag):
            return self.matchTag(exp, actual)
        elif isinstance(exp, NavigableString):
            return True
    
    def matchTag(self, exp, actual):                
        if exp.name != actual.name:
            return False
        elif len(exp) != len(actual) and not exp.find(text=lambda(x): x.startswith("*")):
            return False
        else:
            # test attributes
            for attr in exp.attrs:                
                try:              
                    actual_value = actual[attr[0]]
                    if attr[1][0]!= '$' and actual_value != attr[1]:
                        return False
                except:
                    return False
            # test child tag
            i = 0
            j = 0
            while i < len(exp):
                exp_c = exp.contents[i]
                if self.isAsterisk(exp_c):                    
                    # there is more tags after the asterisk
                    if i+1 !=  len(exp):
                        next_c = exp.contents[i+1]
                        while isinstance(actual.contents[j], NavigableString) or actual.contents[j].name != next_c.name:
                            j+=1
                        if not self.matchAsterisk(exp_c, actual.contents[i:j]):
                            return False
                    else:
                        v = self.matchAsterisk(exp_c, actual.contents[j:])
                        j = len(actual) - 1
                        return v
                else:
                    if not self.matchByType(exp_c, actual.contents[j]):
                        return False
                    j+=1
                i+=1
            if j < len(actual):
                return False
            return True
        
    def isAsterisk(self, tag):
        return isinstance(tag, NavigableString) and str(tag.string)[0] == "*"
        
    def matchAsterisk(self, exp, actual):
        if '$' in exp.string:
            acceptTagNames = exp.string[2:exp.string.index('$')-1]
        else:
            acceptTagNames = exp.string[2:-1]
        if len(acceptTagNames) == 0:
            return True
        else:
            acceptTagNames = acceptTagNames.split(",")            
            for actual_sub in actual:
                if isinstance(actual_sub, Tag) and not actual_sub.name in acceptTagNames:
                    return False
        return True
        
    def extract(self, actual):
        ret = {}
        ret.update(self.extractByType(self.pattern, actual))
        return ret
        
    def extractByType(self, exp, actual):        
        if isinstance(exp, Tag):
            return self.extractTag(exp, actual)
        elif isinstance(exp, NavigableString):
            return self.extractText(exp, actual)
    
    def extractTag(self, exp, actual):
        ret = {}
        for attr in exp.attrs:            
            if attr[1][0] == '$': 
                ret[attr[1][1:]] = actual[attr[0]]
                
        i = 0
        j = 0
        while i < len(exp):
            exp_c = exp.contents[i]
            if self.isAsterisk(exp_c):                    
                # there is more tags after the asterisk
                if i+1 !=  len(exp):
                    next_c = exp.contents[i+1]
                    while isinstance(actual.contents[j], NavigableString) or actual.contents[j].name != next_c.name:
                        j+=1
                    ret.update(self.extractAsterisk(exp_c, actual.contents[i:j]))
                else:                    
                    ret.update(self.extractAsterisk(exp_c, actual.contents[j:]))
                    j = len(actual) - 1
            else:
                ret.update(self.extractByType(exp_c, actual.contents[j]))
                j+=1
            i+=1
                
        return ret
    
    def extractText(self, exp, actual):        
        s = exp.string
            
        if s[0] == '$':
            return {s[1:]:actual.string}
        elif s[0] == '*':
            return self.extractAsterisk(exp, actual)
        else:
            return {}
        
    def extractAsterisk(self, exp, actual):
        s = exp.string
        if not '$' in s:
            return {}
        else:
            return {s[s.index('$')+1:]:actual}        