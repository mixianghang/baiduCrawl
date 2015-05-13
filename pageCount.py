#!/bin/python
#-*-coding: utf-8-*-

import urllib
import urllib2
import cookielib
import re
import time

class baidu_Search:
    
    def getPageCounts(self,htmlunicode):
        pattern = re.compile(r'<div class="nums">(.*?)</div>')
        m = pattern.search(htmlunicode)
        pagesCount = ''
        if m:
            pagesCount = m.group(1)
        else:
            print u'不好意思,未查询到该搜索结果!',   
        return pagesCount
    
    def getHtmlUnicode(self,searchurl):
        cj = cookielib.CookieJar();
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
        urllib2.install_opener(opener)
        req = urllib2.Request(searchurl)
        resp = urllib2.urlopen(req) 
        htmlunicode = resp.read().decode('utf-8')
        return htmlunicode
    
    def getCompare(self,products):
        pair = []
        for i in range(0,len(products)):
            for j in range(0,len(products)):
                if (j != i):
                    pair.append(products[i]+u'比'+products[j])
                
        return pair
                
    def Search(self):
        # products = [u'苹果',u'三星',u'小米',u'诺基亚',u'中兴',u'华为',u'酷派',u'联想']
        products = [u'苹果手机',u'三星手机',u'小米手机',u'诺基亚手机',u'中兴手机',u'华为手机',u'酷派手机',u'联想手机']
        pair = self.getCompare(products)
        myfile = open('/Users/apple/Desktop/countBrandMobile.txt','w')
        for item in pair:
            print u'正在计算\"',item,'\"搜索到的页面数...'
            searchurl = 'http://www.baidu.com/'+'s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd='+urllib.quote(item.encode('utf-8'))
            htmlunicode = self.getHtmlUnicode(searchurl)
            pagesCount = self.getPageCounts(htmlunicode)
            if (pagesCount == ''):
                print u'跳过该查询!'
                myfile.write(item.encode('utf-8')+'\n'+u'未查询到结果数,请重新查询'.encode('utf-8')+'\n')
            else:
                print pagesCount
                myfile.write(item.encode('utf-8')+'\n'+pagesCount.encode('utf-8')+'\n')
            myfile.flush()
            time.sleep(1)
            
        myfile.close()
            
    
print u"""
--------------------------------------------
    author: hao-app
    date  : 2015-03-11
    howTo : enter "quit" to quit program
    advert: 按下任意键来浏览,按下quit退出
--------------------------------------------
"""
if __name__ == '__main__':
    myBaidu = baidu_Search()
    raw_input(u'press enter to search: ')
    myBaidu.Search()
