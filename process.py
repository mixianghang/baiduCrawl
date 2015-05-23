#!/bin/python
#-*-coding: utf-8-*-

import jieba

def cut_sentence(filepath):
    srcfile = open(filepath, 'r')
    enable = True
    sents = []
    while enable:
        line = srcfile.readline().decode('utf-8')
        if (line == ''):
            enable = False
        start = 0
        i = 0
        # punt_list = ',.!?:;~，。！？：；～ \n'.decode('utf-8') #
        # 最后包含了一个空格,前面加u.就不用decode
        punt_list = u'.!?;:~。！？；～\n'  # 不从逗号/空格分开句子
        token = ''
        for word in line:
            # 检查标点符号下一个字符是否还是标点
            if word in punt_list and token not in punt_list:
                sents.append(line[start:i + 1])
                start = i + 1
                i += 1
            else:
                i += 1
                token = list(line[start:i + 2]).pop()  # 取下一个字符
        if start < len(line):
            sents.append(line[start:])
    srcfile.close()
    print u'共拆分', len(sents), u'个句子'
    return sents


def write_word_frequency(dictpath, storepath):
    # 把txt文件里面的词存储成一个数组
    txt_file = open(dictpath, 'r')
    txt_tmp = txt_file.read()
    dict_data = txt_tmp.decode('utf-8').split(u'\n')
    txt_file.close()
    userdict = open(storepath, 'w')
    for word in dict_data:
        userdict.write(word.encode('utf-8') + ' 3' + '\n')
    userdict.close()


def segSent(sents):
    punt_list = u',.!?:;"~{}[]/，“”。！？：；～\n '
    sent_seg_list = []
    jieba.load_userdict('/Users/apple/Desktop/myDiction.txt')
    for sen in sents:
        sen_segs = jieba.cut(sen)
        tem = [s for s in sen_segs if s not in punt_list]
        sent_seg_list.append(tem)
    print u'共对', len(sent_seg_list), u'个句子分词,每个句子分词为一个list'
    '''
    desfile = open(u'/Users/apple/Desktop/sent_seg_list.txt','w')
    for s in sent_seg_list:
        # or: desfile.writelines((' '.join(s)).encode('utf-8')+'\n')
        desfile.writelines(word.encode('utf-8') + ' ' for word in s)
        desfile.writelines('\n')
    desfile.close()
    '''
    return sent_seg_list


def uniSegSents(sent_seg_list, productA, productB):
    des_A = productA[0]
    des_B = productB[0]
    compare_word = [u'对比', u'比较', u'v', u'vs', u'V', u'VS',
                    u'相比', u'相对', u'超过', u'强于', u'高于', u'好于', u'优于', u'大于']
    for s in sent_seg_list:
        for p in productA:
            index = [i for i, w in enumerate(s) if w == p]
            for i in index:
                s[i] = des_A
        for p in productB:
            index = [i for i, w in enumerate(s) if w == p]
            for i in index:
                s[i] = des_B
        for c in compare_word:
            index = [i for i, w in enumerate(s) if w == c]
            for i in index:
                s[i] = u'比'
    return sent_seg_list


def CompeteSent(sent_seg_list, contain_term):
    count = 0
    compete_sent_seg = []
    for sen_segs in sent_seg_list:
        flag = False
        for term in contain_term:
            if term in sen_segs:
                flag = True
            else:
                flag = False
                break
        if (flag == True):
            str = ''.join(sen_segs)
            print str
            compete_sent_seg.append(sen_segs)
            count += 1
    outfile = open(u'/Users/apple/Desktop/CompeteSent.txt', 'w')
    for c in compete_sent_seg:
        outfile.writelines((' '.join(c)).encode('utf-8') + '\n')
    outfile.close()
    print u'共找到两种产品同时出现的比较句数为: ', count
    return count, compete_sent_seg


if __name__ == "__main__":
    # txtpath = '/Users/apple/Desktop/苹果比小米.txt'
    # write_word_frequency('/Users/apple/Desktop/mydict.txt','/Users/apple/Desktop/dict.txt')
    txtpath = raw_input(
        u'enter the absolute or relative abstract file path for process:')
    sents = cut_sentence(txtpath)
    sent_seg_list = segSent(sents)

    productA = [u'苹果', u'iPhone', u'iphone', u'iphone5s', u'iphone5',
                u'iphone4', u'iphone4s', u'iPhone5', u'iPhone5s', u'iphone6', u'iPhone6']
    productB = [u'三星', u'Galaxy', u'GALAXY']
    # productB = [u'小米',u'红米']

    # productA = [u'小米',u'红米']
    # productB = [u'华为',u'荣耀']
    # productB = [u'联想',u'']
    # productB = [u'中兴',u'']

    # productA = [u'三星',u'Galaxy',u'GALAXY']
    # productB = [u'华为',u'荣耀']
    # productB = [u'联想',u'']
    # productB = [u'小米',u'红米']
    # productB = [u'中兴',u'']

    uni_seg_list = uniSegSents(sent_seg_list, productA, productB)
    contain_term = [u'苹果', u'比', u'三星']
    # contain_term = [u'苹果',u'比',u'小米']
    # contain_term = [u'小米',u'比',u'华为']
    # contain_term = [u'小米',u'比',u'联想']
    # contain_term = [u'小米',u'比',u'中兴']
    # contain_term = [u'三星',u'比',u'华为']
    # contain_term = [u'三星',u'比',u'联想']
    # contain_term = [u'三星',u'比',u'小米']
    # contain_term = [u'三星',u'比',u'中兴']
    count, compete_sent_seg = CompeteSent(uni_seg_list, contain_term)
