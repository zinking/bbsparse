# -*- coding: utf-8 -*-
import re;
parse_time_limit = 26*1000;#in millisceonds currently, GAE has limited the request to be finished within 30 seconds

PARSE_USE_XPATH = 1;
PARSE_USE_REGEX = 2;

SINA_163_USERNAME   = 'zinking3@hotmail.com';
SINA_163_PASSWORD   = 'sldfai2-_dak8?';
TWITTER_API_USERNAME    = 'bbstop10';
TWITTER_API_PASSWORD    = '!@#$%^';
BITLY_API_USERNAME      = 'bbstop10';
BITLY_API_APIKEY        = 'R_a4fb86c8c3e20ea6d9d83ef36ff023d7';

sjtubbs = {
    'locate':'http://bbs.sjtu.edu.cn/php/bbsindex.html',
    'root':'http://bbs.sjtu.edu.cn/',
    'dom_row_pattern' :"""
        <tr>             <td >[<a href="*">$board</a>]</td>             <td><a href="$titlelink">$title</a></td>             <td>$author</td>             </tr>
    """,
    'bbsname':'sjtu',
    'schoolname':u'上海交通大学',
    'chinesename':u'饮水思源',
    'rank':1,
    'type':PARSE_USE_REGEX,
    're':r'<td valign="middle"><font color="#FFFFFF"><img src="iconT.gif"> <b>.*?</b></font></td>\n                                </tr>\n                \t\t</table>\n                \t</td>\n                  </tr>.*?</table>',
};
     
newsmth = {
    'locate':'http://www.newsmth.net/rssi.php?h=1',
    'root':'',
    'bbsname':'smth2',
    'schoolname':u'清华大学',
    'chinesename':u'水木社区',
    'dom_row_pattern' : """
        <item>
        <title>$title</title>
        <link>$titlelink</link>
        <author>$author</author>
        <pubDate>*</pubDate>
        <guid>*</guid>
        <description>*</description>
        </item>
    """,
    're':r'<rss version="2.0">.*?</rss>',
    're_board':r'\[(?P<board>.*?)\] (?P<title>.*)',
    'encoding':'utf8',
    'rank':2,
    'type':PARSE_USE_REGEX,
}; 

tjbbs = {
    'locate':'http://bbs.tongji.edu.cn/rssi.php?h=1',
    'root':'',
    'bbsname':'tongji',
    'schoolname':u'同济大学',
    'chinesename':u'同舟共济',
    'dom_row_pattern' : """
        <item>
        <title>$title</title>
        <link>$titlelink</link>
        <author>$author</author>
        <pubDate>*</pubDate>
        <guid>*</guid>
        <description>*</description>
        </item>
    """,
    're':r'<rss version="2.0">.*?</rss>',
    're_board':r'\[(?P<board>.*?)\] (?P<title>.*)',
    'encoding':'utf8',
    'rank':25,
    'type':PARSE_USE_REGEX,
}; 
    
lilybbs = {
    'locate':'http://bbs.nju.edu.cn/bbstop10',
    'root':'http://bbs.nju.edu.cn/',
    'bbsname':'lily',
    'schoolname':u'南京大学',
    'chinesename':u'小百合',
    'dom_row_pattern' : """
        <tr>
        <td>*
        <td><a href="*">$board</a>
        <td><a href="$titlelink">$title</a>
        <td><a href="*">$author</a>
        <td>$postcount
    """,
    're':r'<table width=640>.*?</table>',
    'rank':5,
    'type':PARSE_USE_REGEX,
};
    
zjubbs = {
    'locate':'http://www.freecity.cn/agent/top10.do',
    'root':'http://www.freecity.cn/agent/',
    'bbsname':'zju',
    'schoolname':u'浙江大学',
    'chinesename':u'飘渺水云间',
    'dom_row_pattern' : """
        <tr>
        <td>*</td>
        <td><a href="*">$board</a></div>
        <td>
            <a href="$titlelink">$title</a>
            *
        </td>
        <td><a onclick="*">$author</a></td>
        <td>*</td>
        <td>$postcount</td>
        <td>*</td>
        </tr>
    """,
    're':r'<table .*?>.*?</table>',
    'rank':24,
    'type':PARSE_USE_REGEX,  
};
    
fudanbbs = {
    'locate':'http://bbs.fudan.edu.cn/bbs/top10',
    'root':'http://bbs.fudan.edu.cn/bbs/tcon?board=%s&f=%s',
    'xpath':'/bbstop10 ',
    'bbsname':'fudan',
    'schoolname':u'复旦大学',
    'chinesename':u'日月光华',
    'dom_row_pattern' : """
        <top board='$board' owner='$author' count='$postcount' gid='$titlelink'>$title</top>
    """,
    're':r"<bbstop10>.*?</bbstop10>",
    'rank':3,
    'type':PARSE_USE_REGEX,
    'additional':'special',
};
    
xjtubbs = {
    'locate':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/bbstop10',
    'root':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/',
    'bbsname':'xjtu',
    'schoolname':u'西安交通大学',
    'chinesename':u'兵马俑',
    'dom_row_pattern' : """
        <tr>
        <td>*</td>
        <td><a href="*">$board</a></td>
        <td><a href="$titlelink">$title</a></td>
        <td>$postcount</td>
        </tr>
    """,
    're':r'<table border=1>.*?</table>',
    'rank':12,
    'type':PARSE_USE_REGEX,
};

whubbs = {
    'locate':'http://bbs.whu.edu.cn/rssi.php?h=1',
    'root':'',
    'xpath':'/html/body/div[2]/table/tr/td/fieldset',
    'bbsname':'whu',
    'schoolname':u'武汉大学',
    'chinesename':u'珞珈山水',
    'dom_row_pattern' : """
        <item>
        <title>$title</title>
        <link>$titlelink</link>
        <author>$author</author>
        <pubDate>*</pubDate>
        <guid>*</guid>
        <description>*</description>
        </item>
    """,
    're':r'<rss version="2.0">.*?</rss>',
    're_board_t':r'\[(?P<board>.*?)\] (?P<title>.*)',  
    'encoding':'utf8',
    'rank':10,
    'type':PARSE_USE_REGEX,
};
    
xmubbs = {
    'locate':'http://bbs.xmu.edu.cn/mainpage.php',
    'root':'http://bbs.xmu.edu.cn/',
    'bbsname':'xmu',
    'schoolname':u'厦门大学',
    'chinesename':u'鼓浪听涛',
    'xpath':'/html/body/table[2]/tr/td/table[3]',
    'dom_row_pattern' : """
    <tr>
    <td>
    *
    <a href="*">$board</a>
    *
    <a href="$titlelink">$title</a>
    </td>
    <td>
    <a href="*">$author</a>
    *
    </td>
    </tr>
    """,
    'rank':23,
    'type':PARSE_USE_XPATH,
}; 
    
    
ustcbbs = {
    'locate':'http://bbs.ustc.edu.cn/cgi/bbstop10',
    'root':'http://bbs.ustc.edu.cn/cgi/',
    'xpath':'/html/center/table',
    'bbsname':'ustc',
    'schoolname':u'中国科学技术大学',
    'chinesename':u'瀚海星云',
    'dom_row_pattern' : """
        <tr>
        <td>*
        <td><a href="*">$board</a>
        <td><a href="$titlelink">$title</a>
        <td><a href="*">$author</a>
        <td>$postcount
    """,
    're':r'<table border=0 width=90%>.*?</table>',
    'rank':7,
    'type':PARSE_USE_REGEX,
};
    
sysubbs = {
    'locate':'http://bbs.sysu.edu.cn/bbstop10',
    'root':'http://bbs.sysu.edu.cn/',
    'bbsname':'sysu',
    'schoolname':u'中山大学',
    'chinesename':u'逸仙时空',
    'dom_row_pattern' : """
    <tr> 
    <td>*</td>
    <td>
    <a href="*">$board</a>
    </td>
    <td>
    <a href='$titlelink'>$title</a>
    </td>     
    <td>
    <a href="*">$author</a>
    </td>
    <td>$postcount</td>
    </tr>
    """,
    're':r'<table width="100%" border="0" cellspacing="0" cellpadding="0" height="">.*?</table>', 
    'rank':8,
    'type':PARSE_USE_REGEX,
};
    
dlutbbs = {
    'locate':'http://bbs.dlut.edu.cn/rssi.php?h=1',
    'root':'',
    'bbsname':'dlut',
    'schoolname':u'大连理工大学',
    'chinesename':u'碧海青天',
    'dom_row_pattern' : """
        <item>
        <title>$title</title>
        <link>$titlelink</link>
        <author>$author</author>
        <pubDate>*</pubDate>
        <guid>*</guid>
        <description>*</description>
        </item>
    """,
    're':r'<rss version="2.0">.*?</rss>',
    're_board':r'\[(?P<board>.*?)\] (?P<title>.*)', 
    'encoding':'utf8',
    'rank':24,
    'type':PARSE_USE_REGEX,
}; 

njuptbbs = {
    'locate':'http://bbs.njupt.edu.cn/cgi-bin/bbstop10',
    'root':'http://bbs.njupt.edu.cn/cgi-bin/',
    'bbsname':'njupt',
    'schoolname':u'南京邮电大学',
    'chinesename':u'紫金飞鸿',
    'dom_row_pattern' : """
        <tr>
        <td>*
        <td><a href="*">$board</a>
        <td><a href="$titlelink">$title</a>
        <td><a href="*">$author</a>
        <td>$postcount
    """,
    're':r'<table border=1 width=610>.*?</table>', 
    'rank':13,
    'type':PARSE_USE_REGEX,
};
    
csubbs = {
    'locate':'http://bbs.csu.edu.cn/bbs/',
    'root':'http://bbs.csu.edu.cn/bbs/',
    'bbsname':'csu',
    'schoolname':u'中南大学',
    'chinesename':u'云麓园',
    'dom_row_pattern' : """
       <li><span><a href='*' *>$author</a></span><a href='$titlelink' title='$title' *>*</a></li>
    """,
    're':'<div class="homegridslist" id="homegrids_c_3">.*?</div>', 
    'rank':19,
    'type':PARSE_USE_REGEX,
}; 

jlubbs = {
    'locate':'http://bbs.jlu.edu.cn/cgi-bin/bbssec',
    'root':'http://bbs.jlu.edu.cn/cgi-bin/',
    'xpath':'/html/body/table/tr/td/table/tr[4]/td/table/tr/td[2]/table',
    'bbsname':'jlu',
    'schoolname':u'吉林大学',
    'chinesename':u'牡丹园',
    'dom_row_pattern' : """
        <tr>
        <td>*<a href="$titlelink">$title</a>
        </td>
        </tr>   
    """,
    're_board':r'board=(?P<board>.*?)&', 
    'rank':11,
    'type':PARSE_USE_XPATH,
};

bjtubbs = {
    'locate':'http://forum.byr.edu.cn/wForum/index.php',
    'root':'http://forum.byr.edu.cn/wForum/',
    'bbsname':'bjtu',
    'schoolname':u'北京邮电大学',
    'chinesename':u'北邮人',
    'dom_row_pattern' : """
        <a href="$titlelink">$title</a>
        *
        <font color="red">$postcount</font>
        *
        <br> """,
    're_board':r'board.*?=(?P<board>.*?)&',
    'rank':13,
    'type':PARSE_USE_REGEX,
    'status':3,
};

rucbbs = {
    'locate':'http://bbs.ruc.edu.cn/wForum/topten.php',
    'root':'http://bbs.ruc.edu.cn/wForum/',
    'bbsname':'ruc',
    'schoolname':u'中国人民大学',
    'chinesename':u'天地人大',
    'xpath':'/html/body/table[4]',
    'dom_row_pattern' : """
        <tr>
        <td>*</td>
        <td>&nbsp;<a href="*">$board</a></td>
        <td>&nbsp;<a href="$titlelink">$title</a></td>
        <td><a href="*">$author</a></td>
        <td>&nbsp;$postcount</td>
        </tr>
    """,
    'rank':21,
    'type':PARSE_USE_XPATH,
}; 

seubbs = {
    'locate':'http://bbs.seu.edu.cn/mainpage.php',
    'root':'http://bbs.seu.edu.cn/',
    'bbsname':'seu',
    'schoolname':u'东南大学',
    'chinesename':u'虎踞龙蟠',
    'dom_row_pattern' : """
    <li>
    <a href="$titlelink">$title</a>
    </li>
    """,
    're':r'<h3>\xe4\xbb\x8a\xe6\x97\xa5\xe5\x8d\x81\xe5\xa4\xa7\xe7\x83\xad\xe7\x82\xb9\xe8\xaf\x9d\xe9\xa2\x98</h3>\n\t\t\t<ul>.*?</ul>', 
    're_board1':r'board.*?=(?P<board>.*?)&', 
    'rank':20,
    'type':PARSE_USE_REGEX,
};

scubbs = {
    'locate':'http://www.lsxk.org/rssi.php?h=1',
    'root':'',
    'bbsname':'scu',
    'schoolname':u'四川大学',
    'chinesename':u'蓝色星空',
    'dom_row_pattern' : """
        <item>
        <title>$title</title>
        <link>$titlelink</link>
        <author>$author</author>
        <pubDate>*</pubDate>
        <guid>*</guid>
        <description>*</description>
        </item>
    """,
    're':r'<rss version="2.0">.*?</rss>', 
    're_board':r'\[(?P<board>.*?)\] (?P<title>.*)', 
    'encoding':'utf8',
    'rank':12,
    'type':PARSE_USE_REGEX,
}; 

hitbbs = {
    'locate':'http://www.lilacbbs.com/',
    'root':'',
    'bbsname':'hit',
    'schoolname':u'哈尔滨工业大学',
    'chinesename':u'紫丁香社区',
    'dom_row_pattern' : """
        <li><a href="$titlelink" title="$title" target="_blank">*</a></li>
    """,
    're':r'<div id="portal_block_302_content" class="content">.*?</div>', 
    'encoding':'utf8',
    'rank':14,
    'type':PARSE_USE_REGEX,
}; 

sdubbs = {
    'locate':'http://bbs.sdu.edu.cn/mainpageblue.php',
    'root':'http://bbs.sdu.edu.cn',
    'bbsname':'sdu',
    'schoolname':u'山东大学',
    'chinesename':u'泉韵心声',
    'xpath':'/html/body/div/table[2]/tr[2]/td/table[2]/tr/td',
    'dom_row_pattern' : """
    <li>
    <a href="$titlelink">$title</a>
    *
    <a href="*">$author</a>
    *
    <a href="*">$board</a>
    *
    </li>
    """,
    'rank':16,
    'type':PARSE_USE_XPATH,
};


tjubbs = {
    'locate':'http://bbs.tju.edu.cn/TJUBBSFPKEHPUMNSALVFGWTYHVMRLBXCBIYPKFA_A/bbstop10',
    'root':'http://bbs.tju.edu.cn/TJUBBSFPKEHPUMNSALVFGWTYHVMRLBXCBIYPKFA_A/',
    'bbsname':'tju',
    'schoolname':u'天津大学',
    'chinesename':u'天大求实',
    'dom_row_pattern' : """
    <tr>
    <td>*</td>
    <td>
    <a href='*'>$board</a>
    </td>
    <td>
    <a href='$titlelink'>$title</a>
    </td>
    <td>$postcount</td>
    </tr>
    """,
    're':r'<table class=tb3>.*?</table>', 
    'rank':18,
    'type':PARSE_USE_REGEX,
};

buaabbs = {
    'locate':'http://bbs.buaa.edu.cn/mainpage.php',
    'root':'http://bbs.buaa.edu.cn/',
    'bbsname':'buaa',
    'schoolname':u'北京航空航天大学',
    'chinesename':u'未来花园',
    'dom_row_pattern' : """
    <tr><td class="HotTitle">
    [<a href="*">$board</a>]
    <a href="$titlelink">$title </a></td><td class="HotAuthor"><a href="*">$author</a>&nbsp;&nbsp;</td></tr>
    """,
    're':r'<table border="0" cellpadding="0" cellspacing="0" class="HotTable" align="center">.*?</table>', 
    'rank':22,
    'type':PARSE_USE_REGEX,
};

lzubbs = {
    'locate':'http://bbs.lzu.edu.cn/mainpage.php',
    'root':'http://bbs.lzu.edu.cn/',
    'bbsname':'lzu',
    'schoolname':u'兰州大学',
    'chinesename':u'西北望',
    'xpath':'/html/body/table[3]/tr[2]/td/table[2]/tr/td/table/tr',
    'dom_row_pattern' : """
    <li>
    [<a href="*">$board</a>]
    <a href="$titlelink">$title</a>
    *
    <a href="*">$author</a>
    *
    </li>
    """,
    'rank':28,
    'type':PARSE_USE_XPATH,
};

caubbs = {
    'locate':'http://wusetu.cn/WSTAMnACUKGSZERBGBTWPARKFXGTBPZIFMVFLTVK_A/bbsboa?secstr=?',
    'root':'http://wusetu.cn/WSTAMnACUKGSZERBGBTWPARKFXGTBPZIFMVFLTVK_A/',
    'bbsname':'cau',
    'schoolname':u'中国农业大学',
    'chinesename':u'五色土',
    'xpath':'/html/body/tr[7]/td',
    'dom_row_pattern' : """
    <tr>
    <td>
    <a href='*'>$board</a>
    </td>
    <td>
    <a href='$titlelink'>$title</a>
    </td>
    <td>
    *
    </td>
    <td>
    <a href='*'>$author</a>
    </td>
    <td>
    </td>
    </tr>
    """,
    'rank':32,
    'type':PARSE_USE_XPATH,
};

ustbbbs = {
    'locate':'http://bbs.ustb.edu.cn/mainpage.php',
    'root':'http://bbs.ustb.edu.cn/',
    'bbsname':'ustb',
    'schoolname':u'北京科技大学',
    'chinesename':u'幻想空间',
    'xpath':'/html/body/table[3]/tr[2]/td/p/table[4]',
    'dom_row_pattern' : """
    <tr>
    <td>
    *
    <a href="*">$board</a>
    *
    <a href="$titlelink">$title</a>
    </td>
    <td>
    <a href="*">$author</a>
    *
    </td>
    </tr>
    """,
    'rank':42,
    'type':PARSE_USE_XPATH,
};
           
uestcbbs = {
    'locate':'http://bbs.uestc.edu.cn/cgi-bin/bbstop10',
    'root':'http://bbs.uestc.edu.cn/cgi-bin/',
    'bbsname':'uestc',
    'schoolname':u'电子科技大学',
    'chinesename':u'一往情深',
    'xpath':'/html/table',
    'dom_row_pattern' : """
    <tr>
    <td>*</td>
    <td>
    <a href="*">$board</a>
    </td>
    <td>
    <a href="$titlelink">$title</a>
    </td>
    <td>
    <a href="*">$author</a>
    </td>
    <td>$postcount</td>
    </tr>
    """,
    'rank':43,
    'type':PARSE_USE_XPATH,
};
    
bbs_setting_list = [  newsmth,sjtubbs , jlubbs, xmubbs , sdubbs, seubbs,  lzubbs, caubbs ,
zjubbs, lilybbs, fudanbbs, ustcbbs, sysubbs, whubbs, xjtubbs, scubbs, hitbbs ,
tjubbs, csubbs, buaabbs, dlutbbs, njuptbbs, bjtubbs, tjbbs, ustbbbs, uestcbbs , rucbbs];


