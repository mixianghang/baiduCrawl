#!/bin/python
#-*-coding: utf-8-*-

import urllib
import urllib2
import cookielib
import re
import sys

class baidu_Search:

    def __init__(self):
        self.enable = True
    
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
        
    def Search(self,page,beginurl,targetFile):
        page = int(page)
        beginurl = beginurl
        targetFile = targetFile
        cj = cookielib.CookieJar();
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
        urllib2.install_opener(opener)
        resp = urllib2.urlopen(beginurl)
        htmlunicode = resp.read().decode('utf-8')
        myfile = open('/Users/apple/Desktop/'+targetFile+'.txt','a')

        while self.enable:
            print u'正在准备第',page,'页内容,回车保存文件,输入【quit】退出:'
            myInput = raw_input()
            if (myInput== 'quit'):
                myfile.close()
                break  
            titles_abstracts = self.getTitles_Abstracts(htmlunicode)
            for index in range(len(titles_abstracts)):
                print u"保存第",page,"页第",index+1,"个搜索结果..."
                myfile.writelines(titles_abstracts[index][1].encode('utf-8')+'\n')
                myfile.flush()
            
            nextPageUrl = self.getNextPageUrl(htmlunicode)
            print u'下一页URL是: ',nextPageUrl
            page += 1
            if (nextPageUrl == ''):
                myfile.close()
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
    page = raw_input(u'enter next page to begin: ')
    nexturl = raw_input(u'past next url to begin: ')
    targetFile = raw_input(u'enter the target file name to begin: ')
    myBaidu.Search(page,nexturl,targetFile)
