#-*- coding:utf-8-*-
__author__ = 'kongnian'

import urllib
import re
import requests

url_name = [] #放置视频和名字的空列表
def get():
    url = 'http://www.budejie.com/video/'
    headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'}
    html = requests.get(url,headers=headers).text
    #获取最大盒子的内容
    url_content = re.compile(r'<div class="j-r-list-c">.*?</div>.*?</div>',re.S)
    url_contents = re.findall(url_content,html)
    for i in url_contents:
        url_reg = r'data-mp4="(.*?)">' #地址
        url_items = re.findall(url_reg,i)
        if url_items: #视频存在
            name_reg = re.compile(r'<a href="/detail-.{8}?.html">(.*?)</a>',re.S)
            name_items = re.findall(name_reg,i)
            for i,k in zip(name_items,url_items):
                url_name.append([i,k])
                print i,k

    for i in url_name:
        #i[1]指url,i[0]指name
        urllib.urlretrieve(i[1],'videos//%s.mp4' % i[0])

a = get()