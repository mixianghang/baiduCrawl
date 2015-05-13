#!/bin/python
#-*-coding: utf-8-*-

from __future__ import division
import re

def getNums(file):
    myfile = open(file,'r')
    enable = True
    nums = []
    while enable:
        line = myfile.readline().decode('utf-8')
        if (line == ''):
            enable = False
        pattern = re.compile(r'.*?(\d+.*\d+).+?')
        m = pattern.search(line)
        if (m):
            num = m.group(1)
            num = re.sub(r',','',num)
            nums.append(int(num))
    # for num in nums:
    #   print num,'\t',
    return nums
    
def toNumTable(nums,products):
    # 目的是把7*8转成8*8,如果当初count.py时查询过同类产品比较,或者手动在count文件中加入同类比较数字为0,则可以省去这一步
    n = 0
    table = []
    for i in range(len(products)):
        line_list = []
        for j in range(len(products)):
            if (i == j):
                line_list.append(0)
            else:
                line_list.append(nums[n])
                n += 1
        table.append(line_list)
    # print len(table)
    return table
            
def getCompare(products):
    pair = []
    for i in range(len(products)):
        for j in range(len(products)):
            pair.append(products[i]+u'比'+products[j])
    # print len(pair)
    return pair

def toDict(pair,table):
    mdict = {}
    noSamePair = []
    counts = []
    pairPK = []
    for i in range(len(table)):
        for j in range(i+1,len(table)):
            counts.append(table[i][j]+table[j][i])
            noSamePair.append(pair[i*8+j])
            pairPK.append((pair[i*8+j]+u'/'+pair[j*8+i], str(table[i][j])+u'/'+str(table[j][i]), table[i][j]/table[j][i]))
    
    for n in range(len(noSamePair)):
        mdict[noSamePair[n]] = counts[n]
    return mdict, pairPK
    
def sort_by_value(d): 
    itemslist = d.items()
    # items()函数返回元组list: [('苹果与三星',172938990000),...]
    backlist = []
    for i in itemslist:
        backlist.append([i[1],i[0]])
        # backlist.append((i[1]),i[0]))一样,前者得到[[111,'e'],[221,'w'],...],后者得到[(111,'e'),(221,'w'),...].both can be get by i[1][0]
    backlist.sort(reverse=True)
    return backlist


if __name__=="__main__":
    
    nums = getNums(raw_input(u'enter the absolute path of your txt file containing nums: '))
    # nums = getNums('/Users/apple/Desktop/data/countBrandMobile.txt')
    products = [u'苹果',u'三星',u'小米',u'诺基亚',u'中兴',u'华为',u'酷派',u'联想']
    table = toNumTable(nums,products)
    pair = getCompare(products)
    print '\n\n\t',u'检索页面数如下:\n'
    for i in range(len(products)):
        for j in range(len(products)):
            print ('\t%s\t: \t%*d' %(pair[i*8+j],9,table[i][j]))

    mdict, pairPK = toDict(pair,table)
    # 按照key进行排序
    # print sorted(mdict.items(), key=lambda d: d[0]) 
    # 按照value进行排序
    # print sorted(mdict.items(), key=lambda d: d[1])
    # print mdict.items()
    backlist = sort_by_value(mdict)
    # myfile = open('/Users/apple/Desktop/formatCount.txt','w')
    print '\n\n\t',u'各对产品对比的检索结果总数（热门指数）:\n'
    for b in backlist:
        # print ('%s\t' %b[1]),b[0]
        print ('\t%-s\t: \t%9d' %(b[1]+u'共',b[0]))
        # myfile.write(b[1].encode('utf-8')+'\t:\t'+str(b[0]).encode('utf-8')+'\n')
    
    print '\n\n\t',u'各对产品对比检索结果比值如下:\n'    
    for pk in pairPK:
        print ('\t%-14s\t = %-20s = %f'%(pk[0],pk[1],pk[2]))
        # myfile.write(pk[0].encode('utf-8')+'\t'+pk[1].encode('utf-8')+'\t'+str(pk[2]).encode('utf-8')+'\n')
        
    sortpairPK = []
    for pk in pairPK:
        sortpairPK.append((abs(pk[2]-1.00),pk[0],pk[1]))
        
    sortpairPK.sort()
    print '\n\n\t',u'比值减去1后取绝对值升序排列（差距指数）: \n'
    for ppk in sortpairPK:
        print ('\t%f = \t%-14s\t = %-20s' %(ppk[0],ppk[1],ppk[2]))
        # myfile.write(str(ppk[0]).encode('utf-8')+'\t\t\t'+ppk[1].encode('utf-8')+'\t'+ppk[2].encode('utf-8')+'\n')
    # myfile.close()
