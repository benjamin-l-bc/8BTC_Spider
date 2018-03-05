# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:11:50 2018

@author: v-beshi
"""
import jieba
import get_all_links
import requests
import re
from snownlp import SnowNLP
from bs4 import BeautifulSoup as bs
from matplotlib import pyplot as plt
jieba.add_word('比特币')
jieba.add_word('以太坊')
jieba.add_word('智能合约')
jieba.add_word('虚拟币')
jieba.add_word('区块链')
fakewords=['\n','，','的',' ','。','\r\n','了','是','在','我','\xa0','-','、','有','和','也','你',':','就','都','.','？','：']
def get_key_words(pages):
    sen=[]
    all_title_words={}
    raw_words=[]
    user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers={'User-Agent':user_agent}
    links=get_all_links.get_all_links(pages)
    for link in links:
        page=requests.get(link,headers=headers)
        opt_page=bs(page.text)
        posts=opt_page.find_all('div',class_='t_fsz')
        for i in posts:
            s=SnowNLP(i.get_text())
            sentiment=s.sentiments
            sen.append(sentiment)
            words=jieba.lcut(i.get_text())
            for word in words:
                if word not in fakewords:
                    raw_words.append(word)
    for word in raw_words:
        if word in all_title_words:
            all_title_words[word]+=1
        else:
            all_title_words[word]=1
    title_words=[(all_title_words[j],j) for j in all_title_words]
    title_words.sort()
    title_words.reverse()
    print(title_words)
    print(sen)
    plt.hist(sen)
