#!/bin/python
#-*-coding: utf-8-*-


def uniSegSents(compete_sent_seg):
    feature1 = [u'总评', u'创新力', u'知名度', u'名气', u'品牌']
    feature2 = [u'硬件', u'内存', u'cup', u'电池', u'重量'，u'尺寸',u'材质']
    feature3 = [u'用户体验', u'游戏', u'应用', u'手感', u'外观', u'操控性',u'流畅度', u'售后']
    #feature4 = [u'系统', u'操控性', u'流畅度']
    feaComp1, feaComp2, feaComp3, feaComp4 = [], [], [], [], []
    for c in compete_sent_seg:
        for f in feature1:
            index = [i for i, w in enumerate(c) if w == f]
            if (len(index) != 0):
                for i in index:
                    c[i] = feature1[0]
                feaComp1.append(c)
        for f in feature2:
            index = [i for i, w in enumerate(c) if w == f]
            if (len(index) != 0):
                for i in index:
                    c[i] = feature2[0]
                feaComp2.append(c)
        for f in feature3:
            index = [i for i, w in enumerate(c) if w == f]
            if (len(index) != 0):
                for i in index:
                    c[i] = feature3[0]
                feaComp3.append(c)
        for f in feature4:
            index = [i for i, w in enumerate(c) if w == f]
            if (len(index) != 0):
                for i in index:
                    c[i] = feature4[0]
                feaComp4.append(c)
    return feaComp1, feaComp2, feaComp3, feaComp4


def getScoremydict(filepath):
    fp = open(filepath, 'r')
    mydict = {}
    for line in fp.readlines():
        if (line == '\n'):
            continue
        key, value = (line.decode('utf-8')).replace(u'\n', '').split(' ')
        mydict[key] = value
    return mydict


def scoreSent(feaCompSent, mydict):
    product = [u'苹果', u'三星']
    score, scoreA, scoreB = 0, 0, 0
    for s in feaCompSent:
        index0 = [i for i, w in enumerate(s) if w == product[0]]
        index1 = [i for i, w in enumerate(s) if w == product[1]]
        for w in s:
            if w in mydict.keys():
                score += mydict[w]
        if (index0 < index1):
            scoreA += score
        else:
            scoreB += score
        score = 0
    return scoreA, scoreB
    print product[0], '得分: ', scoreA
    print product[1], '得分: ', scoreB
