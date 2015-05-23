#!/bin/python
#-*-coding: utf-8-*-

import urllib
import urllib2
import cookielib
import re
import sys
# import random

class baidu_Search:

    def __init__(self):
        self.enable = True
        self.page = 0
    
    def rmTags(self,str):
        pattern1 = re.compile(r'<.*?>',re.DOTALL)
        pattern2 = re.compile(r'&nbsp')
        pattern3 = re.compile(ur';-;')
        pattern4 = re.compile(ur'&gt;\s*')
        str = pattern1.sub('',str)
        str = pattern2.sub('',str)
        str = pattern3.sub(u',',str)
        str = pattern4.sub(u'',str)
        return str
        
    def getPageCounts(self,htmlunicode):
        # <div class="nums">百度为您找到相关结果约68,900,000个</div>
        pattern = re.compile(r'<div class="nums">.+?</div>(.*?)</div>')
        m = pattern.search(htmlunicode)
        pagesCount = ''
        if m:
            pagesCount = m.group(1)    
        else:
            print u'不好意思,未查询到任何结果!'     
        return pagesCount
            
    def getNextPageUrl(self,htmlunicode):
        pattern = re.compile(r'<div id="page"\s*>.*?<strong>.*?</strong><a href="(.*?)">')
        m = pattern.search(htmlunicode)
        nextPageUrl = ''
        if m:
            nextPageUrl = 'http://www.baidu.com' + m.group(1)
        else:
            print u"未找到下一页"
        return nextPageUrl
        
    def getTitles_Abstracts(self,htmlunicode):
        patternResults = re.compile(r'<div class="result c-container\s*".*?><h3 class="t"\s*>.*?<div class="c-abstract"\s*>.*?</div>',re.DOTALL)
        # findall在无分组时返回元素为整个匹配字符串的list,在有分组时返回tuple类型的list
        m = patternResults.findall(htmlunicode)
        titles_abstracts = []
        if (m):
            # print m
            for result in m:
                patternTA = re.compile(r'<h3 class="t"\s*>(.*?)</h3>.*?<div class="c-abstract">(.*?)</div>',re.DOTALL)
                mTA = patternTA.search(result)
                if (mTA):
                    title = self.rmTags(mTA.group(1))
                    abstract = self.rmTags(mTA.group(2))
                    titles_abstracts.append((title,abstract))
                else:
                    titles_abstracts.append((u'没有标题',u'没有摘要'))
        else:
            print u'为匹配到标题和摘要'           
        return titles_abstracts
        
    def Search(self,kw):
        kw = kw.decode(sys.stdin.encoding).encode('utf-8')
        searchurl = 'http://www.baidu.com/'+'s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd='+urllib.quote(kw)
        cj = cookielib.CookieJar();
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
        urllib2.install_opener(opener)
        req = urllib2.Request(searchurl)
        """user_agents = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36'
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) /Chrome/28.0.1468.0 Safari/537.36',
                        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)'
                        ]
        r = random.randint(0,7)
        req.add_header('User-agent',user_agents[r])
        """
        resp = urllib2.urlopen(req) 
        htmlunicode = resp.read().decode('utf-8')
        
        # print htmlunicode
        # myfile = open('/Users/apple/Desktop/text.txt','w')
        # myfile.write(htmlunicode.encode('utf-8'))
        pagesCount = self.getPageCounts(htmlunicode)
        print pagesCount

        while self.enable:
            print u'请按[回车键]浏览第',self.page+1,'页内容,输入[quit]退出程序:'
            myInput = raw_input()
            if (myInput== 'quit'):
                break  
            titles_abstracts = self.getTitles_Abstracts(htmlunicode)
            for index in range(len(titles_abstracts)):
                print u"第",self.page+1,"页第",index+1,"个搜索结果..."
                print u"标题: ",titles_abstracts[index][0]
                print u"摘要: ",titles_abstracts[index][1]
                print "\r\n"
                
            nextPageUrl = self.getNextPageUrl(htmlunicode)
            self.page += 1
            # print u'下一页url为:', nextPageUrl
            if (nextPageUrl == ''):
                break
            resp = urllib2.urlopen(nextPageUrl)
            htmlunicode = resp.read().decode('utf-8')
            
if __name__ == '__main__':

    print u"""
--------------------------------------------
    author: hao-app
    date  : 2015-03-11
    howTo : enter "quit" to quit program
    advert: 按下任意键来浏览,按下quit退出
--------------------------------------------
"""
    myBaidu = baidu_Search()
    myBaidu.Search(raw_input(u'enter keyword to search: '))
