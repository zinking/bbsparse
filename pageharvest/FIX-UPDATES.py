# coding=utf-8

from BeautifulSoup      import BeautifulSoup;
from bsoupxpath         import Path;
from customized_soup    import CustomizedSoup;
from scraper            import Scraper;
import re;
import urllib,urllib2,Cookie

""" 
#PATCH ON SJTU V2 - lefted guidance
#GET PATTERN LINE USING REPR
#PRINCIPAL NO.1 YOU CAN FORMAT THE DOM WHEN YOU OBSERVE,BUT WHEN YOU HANLE IT TO MACHINE, PLEASE KEEP IT <B>ORGINAL</B>

pattern = '<td valign="middle"><font color="#FFFFFF"><img src="iconT.gif"> <b>.*?</b></font></td>\n                                </tr>\n                \t\t</table>\n                \t</td>\n                  </tr>.*?</table>'
htmlstring = urllib2.urlopen('http://bbs.sjtu.edu.cn/php/bbsindex.html').read();
htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');
blockstring = re.search(pattern,htmlstring,re.DOTALL).group();
print blockstring;
"""
"""
##PATCH ON FDU V2
url = "http://www.lilacbbs.com/"
#PRINCIPAL NO.2 YOU MAY NEED DOM STRUCTURE TO HELP YOU DETERMINE RE EXPRESSION"
pattern = """"""
htmlstring = urllib2.urlopen(url).read();
htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');

blockstring = re.search(pattern,htmlstring,re.DOTALL).group();
print blockstring;
"""
"""
##PATCH ON SEU
url = "http://bbs.seu.edu.cn/mainpage.php"
#PRINCIPAL NO.2 YOU MAY NEED DOM STRUCTURE TO HELP YOU DETERMINE RE EXPRESSION"
#pattern = "<h3>今日十大热点话题</h3>\n\t\t\t<ul>.*?</ul>"
pattern = "<h3>\xe4\xbb\x8a\xe6\x97\xa5\xe5\x8d\x81\xe5\xa4\xa7\xe7\x83\xad\xe7\x82\xb9\xe8\xaf\x9d\xe9\xa2\x98</h3>\n\t\t\t<ul>.*?</ul>"

htmlstring = urllib2.urlopen(url).read();
htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');

blockstring = re.search(pattern,htmlstring,re.DOTALL).group();
print blockstring;
print repr(pattern);
"""

##PATCH ON BUAA
url = "http://bbs.buaa.edu.cn/mainpage.php"
#PRINCIPAL NO.2 YOU MAY NEED DOM STRUCTURE TO HELP YOU DETERMINE RE EXPRESSION"
#pattern = """<h3>今日十大热点话题</h3>\n\t\t\t<ul>.*?</ul>"""
pattern = '<td class="MainContentText">.*?</td>'

htmlstring = urllib2.urlopen(url).read();
htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');

blockstring = re.search(pattern,htmlstring,re.DOTALL).group();
print blockstring;







    